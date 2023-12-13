import requests
from urllib.parse import urlencode
import sys
import json
from record import Record

this = sys.modules[__name__]
# this.url = 'https://review.osti.gov/elink2api/'
this.url = 'https://dev.osti.gov/elink2api/'
this.api_token = ""

# Define some helpfully-named Exceptions for API issues
class APIException(IOError):
    """ Error or Exception handling a particular request. """

    def __init__(self, *args):
        super(IOError, self).__init__(*args)

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

class ConflictException(APIException):
    """ The url or file already exists on the server. """


def _check_status_code(response):
    if response.status_code in [200, 201, 204]:
        return response
    elif response.status_code == 400:
        raise BadRequestException('Bad request, JSON cannot be interpreted, or validation issues.')
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

def set_api_token(api_token):
    this.api_token = api_token

def set_target_url(url):
    this.url = url


def get_single_record(osti_id):
    response = requests.get(this.url + "records/" + osti_id, headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")
    # response = requests.get('https://review.osti.gov/elink2api/' + "records/" + osti_id, headers={"Authorization": "Bearer " + api_token})

    return _check_status_code(response)

def query_records(params):
    query_params = ""

    if(len(params) > 0):
        query_params = "?" + urlencode(params)

    response = requests.get(f"{this.url}records{query_params}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def reserve_doi(data):   
    response = requests.post(this.url + "records/save", headers={"Authorization": f"Bearer {this.api_token}"}, json=data)
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def submit_new_record(data):
    response = requests.post(f"{this.url}records/submit", headers={"Authorization": f"Bearer {this.api_token}"}, json=data)
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def update_record(osti_id, data, state="save"):
    response = requests.put(f"{this.url}records/{osti_id}/{state}", headers={"Authorization": f"Bearer {this.api_token}"}, json=data)
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def get_revision_by_number(osti_id, revision_number):
    response = requests.get(f"{this.url}records/revision/{osti_id}/at/{revision_number}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def get_revision_by_date(osti_id, date):
    response = requests.get(f"{this.url}records/revision/{osti_id}/dated/{date}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def get_all_revisions(osti_id):
    response = requests.get(f"{this.url}records/revision/{osti_id}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)


def get_media(osti_id=None):
    response = requests.get(this.url + "media/" + osti_id, headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")
    
    return _check_status_code(response)

def get_media_content(media_id):
    response = requests.get(f"{this.url}media/{media_id}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def post_media(osti_id=None, file_path=None, params=None):
    query_params = ""

    if(len(params) > 0):
        query_params = "?" + urlencode(params)

    response = requests.post(f"{this.url}media/{osti_id}{query_params}", headers={"Authorization": f"Bearer {this.api_token}"}, files={'file': file_path})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def put_media(osti_id, media_id, file_path, params=None): #title=None, url=None):
    query_params = ""

    if(len(params) > 0):
        query_params = "?" + urlencode(params)

    response = requests.put(f"{this.url}media/{osti_id}/{media_id}{query_params}", 
                            headers={"Authorization": f"Bearer {this.api_token}"}, 
                            files={'file': open(file_path, 'rb')})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def delete_all_media(osti_id, reason):
    response = requests.delete(f"{this.url}media/{osti_id}?reason={reason}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)

def delete_single_media(osti_id, media_id, reason):
    response = requests.delete(f"{this.url}media/{osti_id}/{media_id}?reason={reason}", headers={"Authorization": f"Bearer {this.api_token}"})
    print(f"Response URL: {response.url}")

    return _check_status_code(response)


def record_to_json(record):
    return record.model_dump_json()

# def dict_to_record(dict_record):
#     testResponse = get("2300000", api_token)
#     return False
