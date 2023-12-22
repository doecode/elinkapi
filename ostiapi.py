import requests
from urllib.parse import urlencode
import sys
import json
from models.record import Record
from models.revisions import RevisionHistory, Revision
from models.media_info import MediaInfo

this = sys.modules[__name__]
# this.url = 'https://review.osti.gov/elink2api/'
this.url = 'https://dev.osti.gov/elink2api/'
this.api_token = ""

# Define some helpfully-named Exceptions for API issues
class APIException(Exception):
    """ Error or Exception handling a particular request. """

    def __init__(self, *args):
        super(Exception, self).__init__(*args)

class NotFoundException(APIException):
    """ Record not on file. """
 
class ForbiddenException(APIException):
    """ Access was forbidden. """

class ServerException(APIException):
    """ Unknown internal server error. """

class UnauthorizedException(APIException):
    """ Unauthorized access attempted. """

class BadRequestException(APIException):
    """ Unable to parse the JSON Request made. """

def convert_error(error):
    error_message = f"Status: {error['status']}\nDetail: {error['detail']}\nSource -> Pointer: {error['source']['pointer']}\n"
    return error_message
class ValidationException(APIException):
    """Adds validation errors from the response to the exception message"""
    def __init__(self, errors_dict):
        self.errors_dict = errors_dict
        super().__init__(self.generate_error_message(self.errors_dict))

    def generate_error_message(self, errors_dict):
        error_message = ""

        for error in errors_dict:
            error_message += convert_error(error) + "\n"

        return error_message

class ConflictException(APIException):
    """ The url or file already exists on the server. """

# Internally used methods
def _check_status_code(response):
    """Evaluates the response and selects the appropriate action based on 
    the status code 

    Arguments:
        response -- response from E-Link 2.0

    Raises:
        UnauthorizedException: API token not provided with request
        ForbiddenException: User is not allowed to access
        NotFoundException: Requested object could not be found
        ConflictException: Resource already exists
        ValidationException: Issue with the submitted json, see error message for details
        ServerException: Unknown error

    Returns:
        Either the successful response or the appropriate exception is raised
    """
    if response.status_code in [200, 201, 204]:
        return response
    elif response.status_code == 400:
        raise ValidationException((json.loads(response.text)["errors"]))
        # raise BadRequestException('Bad request, JSON cannot be interpreted, or validation issues.')
    elif response.status_code == 401:
        raise UnauthorizedException('No user account information supplied.')
    elif response.status_code == 403:
        raise ForbiddenException('User account failed login or authentication.')
    elif response.status_code == 404:
        raise NotFoundException("Record is not on file.")
    elif response.status_code == 409:
        raise ConflictException("Conflict, URL or file is already associated with this record.")
    else: # 500
        raise ServerException('ELINK service is not available or unknown connection error.')

def _convert_response_to_records(response):
    """Returns array of Records"""
    json_records = json.loads(response.text)
    
    if(not isinstance(json_records, list)):
        json_records = [json_records]
    records = [Record(**record) for record in json_records]
    
    return records

def _convert_response_to_media_info(response):
    """returns array of media_info"""
    return_val = []
    all_media_info = json.loads(response.text)

    for media in all_media_info:
        return_val.append(MediaInfo(**media))

    return return_val

def _convert_response_to_revision_history(response):
    """returns array of revision_history"""
    return_val = []
    all_history = json.loads(response.text)
    
    for revision in all_history:
        return_val.append(Revision(**revision))

    return RevisionHistory(**{"revision_history": return_val})


# Start of actual module methods that should be used.

# Setup and helper functions
def set_api_token(api_token):
    """Sets the API Token that will be used in each call"""
    this.api_token = api_token

def set_target_url(url):
    """Sets the target URL/environment you will be making requests to.
    Default= https://review.osti.gov/elink2api"""
    this.url = url

def record_to_dict(record):
    return record.model_dump(exclude_none=True)


def record_to_json(record):
    return record.model_dump_json(exclude_none=True)

# Record Methods
def get_single_record(osti_id):
    """Obtain the metadata JSON for a record at OSTI

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record

    Returns:
        The metadata of a single record
    """
    response = requests.get(this.url + "records/" + osti_id, headers={"Authorization": f"Bearer {this.api_token}"})

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        # returns array, so grab the first element
        return _convert_response_to_records(response)[0]

def query_records(params):
    """Query for records using a variety of query params

    Arguments:
        params -- See https://review.osti.gov/elink2api/#tag/records/operation/getRecords for 
            the list of allowed query parameters. 

    Returns:
        An array of one or more matching metadata records, if found. 
    """
    query_params = ""

    if(len(params) > 0):
        query_params = "?" + urlencode(params)

    response = requests.get(f"{this.url}records{query_params}", headers={"Authorization": f"Bearer {this.api_token}"})
    
    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        return _convert_response_to_records(response)

def reserve_doi(record):
    """ Save a Record with minimal validations: 
        Required:
            title
            site_ownership_code
            product_type

    Arguments:
        record -- Metadata record that you wish to make the new revision of OSTI ID

    Returns:
        Record that has been saved to E-Link 2.0
    """
    response = requests.post(this.url + "records/save", headers={"Authorization": f"Bearer {this.api_token}"}, json=json.loads(record.model_dump_json(exclude_none=True)))

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        return _convert_response_to_records(response)

def post_new_record(record, state="save"):
    """Create a new metadata Record with OSTI

    Arguments:
        record -- Metadata record that you wish to make the new revision of OSTI ID

    Returns:
        Record with the admin fields added
    """
    response = requests.post(f"{this.url}records/{state}", headers={"Authorization": f"Bearer {this.api_token}", "Content-Type": "application/json"}, json=json.loads(record.model_dump_json(exclude_none=True)))

    return_value =_check_status_code(response)

    if(type(return_value) is requests.Response):
        # returns array, so grab the first element
        return _convert_response_to_records(response)[0] 

def update_record(osti_id, record, state="save"):
    """Update existing records at OSTI by unique OSTI ID

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record
        record -- Metadata record that you wish to make the new revision of OSTI ID

    Keyword Arguments:
        state -- The desired submission state of the record ("save" or "submit")  (default: {"save"})

    Returns:
        The updated Record with the given information in data, creating a new revision
    """
    response = requests.put(f"{this.url}records/{osti_id}/{state}", headers={"Authorization": f"Bearer {this.api_token}"}, json=record_to_dict(record))

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        # returns array, so grab the first element
        return _convert_response_to_records(response)[0]

def get_revision_by_number(osti_id, revision_number):
    """Access specific revision number of a given OSTI ID

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record
        revision_number -- The specific revision number to retrieve

    Returns:
        The Record metadata at the given revision number
    """
    response = requests.get(f"{this.url}records/revision/{osti_id}/at/{revision_number}", headers={"Authorization": f"Bearer {this.api_token}"})
    
    # Special case on this exception -> Get 404's when date is before record creation
    if(response.status_code == 404): 
        raise NotFoundException("Requested record version is not on file.")

    return_value =_check_status_code(response)

    if(type(return_value) is requests.Response):
        # returns array, so grab the first element
        return _convert_response_to_records(response)[0]

def get_revision_by_date(osti_id, date):
    """Access revision of metadata by OSTI ID that was active at the given date-time provided

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record
        date -- Date on which you wish to search for a revision of a Record

    Returns:
        The Record metadata on the given date
    """
    response = requests.get(f"{this.url}records/revision/{osti_id}/dated/{date}", headers={"Authorization": f"Bearer {this.api_token}"})

    # Special case on this exception -> Get 404's when date is before record creation
    if(response.status_code == 404): 
        raise NotFoundException("Record version for specified date is not on file.")

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        # returns array, so grab the first element
        return _convert_response_to_records(response)[0]

def get_all_revisions(osti_id):
    """Obtain summary information of all given revisions of a metadata record by its OSTI ID

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record

    Returns:
        All the metadata of the revisions of a record: start/end dates, workflow status, and revision number
    """
    response = requests.get(f"{this.url}records/revision/{osti_id}", headers={"Authorization": f"Bearer {this.api_token}"})

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        return _convert_response_to_revision_history(response)


# Media Methods
def get_media(osti_id):
    """Get information about any media sets (files or URLs) associated with the OSTI ID

    Keyword Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record 

    Returns:
        Metadata info of all the media associated with the osti_id
    """
    response = requests.get(this.url + "media/" + osti_id, headers={"Authorization": f"Bearer {this.api_token}"})

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        return _convert_response_to_media_info(response)

def get_media_content(media_id):
    """Obtain content stream of a particular MEDIA FILE by its unique ID

    Arguments:
        media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record

    Returns:
        Text that is associated with the media_id
    """
    response = requests.get(f"{this.url}media/{media_id}", headers={"Authorization": f"Bearer {this.api_token}"})

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        return json.loads(response.text)

def post_media(osti_id, file_path, params=None):
    """Attach the media found at the given filepath to the record associated
    with the given osti_id. Optionally can provide 2 params: a title for the media file, and, 
    if not providing a file, a url that leads to the media.

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record
        file_path -- Path to the media file that will be attached to the Record 

    Keyword Arguments:
        params -- "title" that can be associated with the media file
                  "url" that points to media if not sending file (default; {None})
        
    Returns:
        A MediaInfo instance, an exception otherwise
    """
    query_params = ""

    if(len(params) > 0):
        query_params = "?" + urlencode(params)

    response = requests.post(f"{this.url}media/{osti_id}{query_params}", headers={"Authorization": f"Bearer {this.api_token}"}, files={'file': file_path})

    return_value =_check_status_code(response)

    if(type(return_value) is requests.Response):
            return _convert_response_to_media_info(response)

def put_media(osti_id, media_id, file_path, params=None):
    """Replace a given media set with a new basis; either a URL or a media file.
    This will replace the previous media set

    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record
        media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record
        file_path -- Path to the media file that will be attached to the Record

    Keyword Arguments:
        params -- "title" that can be associated with the media file
                  "url" that points to media if not sending file (default; {None})

    Returns:
        A MediaInfo instance, an exception otherwise
    """
    query_params = ""

    if(len(params) > 0):
        query_params = "?" + urlencode(params)

    response = requests.put(f"{this.url}media/{osti_id}/{media_id}{query_params}", 
                            headers={"Authorization": f"Bearer {this.api_token}"}, 
                            files={'file': open(file_path, 'rb')})

    return_value =_check_status_code(response)
    
    if(type(return_value) is requests.Response):
        return _convert_response_to_media_info(response)

def delete_single_media(osti_id, media_id, reason):
    """Disassociate an individual media set from this OSTI ID

    Arguments:
        osti_id -- ID that uniquely identifies an E-Link 2.0 Record
        media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record
        reason -- Reason for deleting all media

    Returns:
        True if successful, False/exception otherwise
    """
    response = requests.delete(f"{this.url}media/{osti_id}/{media_id}?reason={reason}", headers={"Authorization": f"Bearer {this.api_token}"})

    return_value =_check_status_code(response)

    if(response.status_code == 204): 
        return True
    return False

def delete_all_media(osti_id, reason):
    """Disassociate ALL media sets from this OSTI ID 
    
    Arguments:
        osti_id -- ID that uniquely identifies an E-link 2.0 Record
        reason -- Reason for deleting all media

    Returns:
        True if successful, False/exception otherwise
    """
    response = requests.delete(f"{this.url}media/{osti_id}?reason={reason}", headers={"Authorization": f"Bearer {this.api_token}"})

    return_value =_check_status_code(response)
    
    if(response.status_code == 204): 
        return True
    return False