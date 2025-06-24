import requests
from urllib.parse import urlencode
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .exceptions import NotFoundException,ForbiddenException,UnauthorizedException,ServerException,ConflictException,BadRequestException
from .record import Record, RecordResponse
from .revision import Revision
from .revision_comparison import RevisionComparison
from .media_info import MediaInfo
from .utils import Validation
from .query import Query
import os
import mimetypes

class Elink:
    """
    Defines a set of access points for E-Link API endpoints.

    Construct an api access object, defining the desired API target and supplying the user-specific API key token.
    Note that Review and Production are entirely separate instances, with Production being the default target if not
    specified.

    These endpoint targets are:
    review: https://review.osti.gov/elink2api/
    production: https://www.osti.gov/elink2api/

    >>> from elinkapi import Elink
    >>> api = Elink(target = "https://review.osti.gov/elink2api/", token=MYUSERTOKEN)

    Use this to access functions, including:

    get_single_record -- obtain a particular Record by its OSTI ID
    query_records -- query E-Link records according to given parameters
    post_new_record -- create a new Record; returned with unique OSTI ID value
    update_record -- update the indicated record content by OSTI ID
    patch_record -- submit a partial JSON update to a given record by its OSTI ID
    patch_json -- submit a JSON-patch set of commands to update a given record by its OSTI ID
    get_media -- obtain all media sets associated with an OSTI ID
    post_media -- add a new media set to the OSTI ID
    put_media -- replace an existing media set with new content

    Record creation methods (reserve_doi, post_new_record, update_record) may provide a user-supplied Record, a dict 
    containing required key elements, or as keyword arguments.
    >>> api.post_new_record(title="My dataset", product_type="DA")
    or
    >>> api.post_new_record({ "title": "New Technical Report", "product_type" : "TR" })
    or
    >>> api.post_new_record(Record(title="Example journal", product_type="JA", journal_name="Science", doi="10.11578/23423"))

    Record instances contain a reference function dict() to obtain a dictionary from its content.  Supply optional
    "exclude_none=True" argument to obtain only elements with values if desired:
    >>> myrecord.dict(exclude_none=True)

    Individual values in Record instances are directly accessible and may be set in the same way; e.g., 
    >>> myrecord.title = "New Title Here"
    or
    >>> print (myrecord.doi)

    """
    def __init__(self, token=None, target=None):
        """
        Set up the E-Link 2 OSTI API connector.
        """
        self.token = token
        self.target = target or "https://www.osti.gov/elink2api/"

    def _convert_response_to_records(self, response):
        """Returns array of Records"""
        json_records = json.loads(response.text)
        
        if(not isinstance(json_records, list)):
            json_records = [json_records]
        records = [RecordResponse(**record) for record in json_records]
        
        return records

    def _convert_response_to_media_info(self, response):
        """returns array of media_info"""
        return_val = []
        all_media_info = json.loads(response.text)

        """ ensure the API response is a singleton or array of media info. """
        if isinstance(all_media_info, dict):
            # singleton instance response
            return_val.append(MediaInfo(**all_media_info))
        else:
            # array of objects
            for media in all_media_info:
                return_val.append(MediaInfo(**media))

        return return_val

    def _convert_response_to_revision_history(self, response):
        """returns array of revision_history"""
        all_history = json.loads(response.text)
        
        if(not isinstance(all_history, list)):
            all_history = [all_history]
        revisions = [Revision(**revision) for revision in all_history]
        
        return revisions

    def _convert_response_to_revision_comparison(self, response):
        """returns array of revision_history"""
        comparison = json.loads(response.text)
        
        revision_comparison = [RevisionComparison(**field_diff) for field_diff in comparison]
        
        return revision_comparison

    # Start of actual module methods that should be used.
    # Setup and helper functions
    def set_api_token(self, api_token):
        """Sets the API Token that will be used in each call"""
        self.token = api_token

    def set_target_url(self, url="https://www.osti.gov/elink2api/"):
        """Sets the target URL/environment you will be making requests to."""
        self.target = url

    def record_to_dict(self, record):
        return record.model_dump(exclude_none=True)

    def record_to_json(self, record):
        return record.model_dump_json(exclude_none=True)

    # Record Methods
    def get_single_record(self, osti_id: int):
        """Obtain the metadata JSON for a record at OSTI.

        >>> record = api.get_single_record(2009785)
        >>> print (record.title)

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record

        Returns:
            Record - metadata of a single record 
        """
        response = requests.get(f'{self.target}/records/{osti_id}',
                                headers = { "Authorization" : f"Bearer {self.token}"})
        Validation.handle_response(response)
        
        # returns array, so grab the first element
        return self._convert_response_to_records(response)[0]

    def query_records(self, **kwargs):
        """Query for records using a variety of query search parameters.

        Example:
        >>> query = api.query_records(title="Science", product_type = "JA")
        >>> query.total_rows
        1738
        >>> for record in query:
        ...   print (record.title)

        Arguments:
            params -- See https://www.osti.gov/elink2api/#tag/records/operation/getRecords for 
                the list of allowed query parameters. 

        Returns:
            a iterative Query object containing total_rows count matching the search, and data containing
            a page at a time of returned Record values as a List.
        """
        query_params = ""

        if(len(kwargs) > 0):
            query_params = "?" + urlencode(kwargs)

        response = requests.get(f"{self.target}/records{query_params}", 
                                headers={"Authorization": f"Bearer {self.token}"})
        
        Validation.handle_response(response)

        return Query(response, target=self.target, token=self.token)

    def reserve_doi(self, r=None, **kwargs):
        """ Save a Record with minimal validations. 

            Required data elements, either via a Record or keyword arguments:
                title
                site_ownership_code
                product_type

            Provided as a convenience; functionally equivalent to post_new_record method, with
            state="save".

            >>> reservation = api.reserve_doi(title="Sample dataset from 2012", product_type = "DA")
            >>> print (reservation.doi)
            '10.11578/2003824'

        Arguments:
            record -- Metadata record that you wish to save to E-Link 2.0 (optional)

        Keyword Arguments:
            if record is not provided, these will be used to construct a new one for DOI reservation.

        Returns:
            Record - metadata of a single record that has been saved to E-Link 2.0
        """
        # perform a minimal new record POST
        return self.post_new_record(r=r, **kwargs)
    
    def _convert_record(self, record=None, **kwargs) -> Record:
        """
        Accept either a Record or a dict, which we convert to a Record for consistency. Will
        take appropriately-named keyword arguments if record is not provided to construct one.

        Arguments:
            record -- either a dict to convert, or already a Record (optional)

        Keyword arguments:
            if record not provided, use these to construct one

        Returns:
            a Record, possibly from the dict if possible.
        
        """
        if record and isinstance(record, dict):
            return Record(**record)
        elif record and isinstance(record, Record):
            return record
        else:
            return Record(**kwargs)

    def post_new_record(self, r=None, state="save", **kwargs):
        """Create a new metadata Record with OSTI

        Arguments:
            record -- Metadata record that you wish to send ("save" or "submit") to E-Link 2.0. May provide as 
                      Record or dict, or as keyword arguments.

        Keyword Arguments:
            state -- The desired submission state of the record ("save" or "submit")  (default: {"save"})
            if record not provided, takes rest of keyword arguments to construct a Record

        Returns:
            Record - metadata of a single record saved (or submitted) to E-Link 2.0
        """
        # make a Record from provided arguments
        record = self._convert_record(record=r, **kwargs)
        # post it as a new record
        response = requests.post(f"{self.target}records/{state}", 
                                 headers={
                                     "Authorization": f"Bearer {self.token}", 
                                     "Content-Type": "application/json" 
                                    }, 
                                 json=json.loads(record.model_dump_json(exclude_none=True)))

        Validation.handle_response(response)

        # returns array, so grab the first element
        return self._convert_response_to_records(response)[0] 
    
    def patch_record(self, osti_id, patch, state="save"):
        """
        Update record via partial-patch-json method endpoint.  Provide only the JSON you wish to alter.

        >>> api.patch_record(2008590, { "title": "This title is new", "description": "As is this description" })

        Arguments:
            osti_id -- the OSTI ID of the record to patch
            patch -- JSON/dict containing the partial JSON to apply

        Keyword arguments:
            state -- the desired workflow submission state ("save" or "submit") default: "save"

        Returns:
            Record -- the metadata of the new record revision if successful
        """
        response = requests.patch(f"{self.target}/records/{osti_id}/{state}",
                        headers = { 
                            "Authorization" : f"Bearer {self.token}",
                            "Content-Type": "application/json"
                        },
                        data=str(patch))
        
        Validation.handle_response(response)

        return self._convert_response_to_records(response)[0]
    
    def patch_json(self, osti_id, jsonpatch, state="save"):
        """
        Update record via a JSON-patch set of command operations.  Note the jsonpatch is intended to be
        an array of one or more operations to perform; those including "add", "replace", "copy", "move", or
        "remove".  See details at https://www.osti.gov/elink2api/#operation/patchRecord.

        >>> api.patch_json(2007439, [{"op": "add", "path": "/description", "value": "A new description."}])
        
        Arguments:
            osti_id -- The OSTI ID of the record to patch
            jsonpatch -- JSON or dict containing any operations to perform on the record

        Keyword arguments:
            state -- Desired workflow state of the new revision ("save" or "submit") default: "save"

        Returns:
            Record -- the metadata of the new revision with operations performed if successful
        """
        response = requests.patch(f"{self.target}/records/{osti_id}/{state}",
                                  headers = {
                                      "Authorization" : f"Bearer {self.token}",
                                      "Content-Type": "application/json-patch+json"
                                  },
                                  data=json.dumps(jsonpatch))
        
        Validation.handle_response(response)

        return self._convert_response_to_records(response)[0]

    def update_record(self, osti_id, r=None, state="save", **kwargs):
        """Update existing records at OSTI by unique OSTI ID.  Note this REPLACES the record entirely;
        the provided record details will become the new revision of the record on file; all required
        information must therefore be provided as applicable.

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            record -- Metadata record that you wish to make the new revision of OSTI ID (optional, as Record or dict)

        Keyword Arguments:
            state -- The desired submission state of the record ("save" or "submit")  (default: {"save"})
            if record not specified, rest of the keyword arguments are used to construct one

        Returns:
            Record - Metadata of record updated with the given information, creating a new revision
        """
        # get a record
        record = self._convert_record(record=r, **kwargs)
        # send the UPDATE
        response = requests.put(f"{self.target}records/{osti_id}/{state}", 
                                headers={
                                    "Authorization": f"Bearer {self.token}"
                                }, 
                                json=json.loads(record.model_dump_json(exclude_none=True)))

        Validation.handle_response(response)
        
        # returns array, so grab the first element
        return self._convert_response_to_records(response)[0]

    def get_revision_by_number(self, osti_id, revision_number):
        """Access specific revision number of a given OSTI ID

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            revision_number -- The specific revision number to retrieve

        Returns:
            Record - The metadata of the Record at the given revision number
        """
        response = requests.get(f"{self.target}records/revision/{osti_id}/at/{revision_number}", 
                                headers={
                                    "Authorization": f"Bearer {self.token}"
                                })
        
        # Special case on this exception -> Get 404's when date is before record creation
        if(response.status_code == 404): 
            raise NotFoundException("Requested record version is not on file.")

        Validation.handle_response(response)

        # returns array, so grab the first element
        return self._convert_response_to_records(response)[0]

    def get_revision_by_date(self, osti_id, date):
        """Access revision of metadata by OSTI ID that was active at the given date-time provided

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            date -- Date on which you wish to search for a revision of a Record

        Returns:
            Record - The metadata of the Record on the given date
        """
        response = requests.get(f"{self.target}records/revision/{osti_id}/dated/{date}", 
                                headers={"Authorization": f"Bearer {self.token}"})

        # Special case on this exception -> Get 404's when date is before record creation
        if(response.status_code == 404): 
            raise NotFoundException("Record version for specified date is not on file.")

        Validation.handle_response(response)
        
        # returns array, so grab the first element
        return self._convert_response_to_records(response)[0]

    def get_all_revisions(self, osti_id):
        """Obtain summary information of all given revisions of a metadata record by its OSTI ID

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record

        Returns:
            RevisionHistory - All the metadata of the revisions of a record
        """
        response = requests.get(f"{self.target}records/revision/{osti_id}", 
                                headers={"Authorization": f"Bearer {self.token}"})

        Validation.handle_response(response)
        
        return self._convert_response_to_revision_history(response)

    def compare_two_revisions(self, osti_id, left, right):
        """Compare values of two separate revisions of the same metadata record

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            left -- The first revision number to retrieve and compare
            right -- The second revision number to retrieve and compare

        Returns:
            List[RevisionComparison]
        """
        response = requests.get(f"{self.target}records/revision/{osti_id}/compare/{left}/{right}", 
                                headers={"Authorization": f"Bearer {self.token}"})

        Validation.handle_response(response)
        
        return self._convert_response_to_revision_comparison(response)


    # Media Methods
    def get_media(self, osti_id):
        """Get information about any media sets (files or URLs) associated with the OSTI ID

        Keyword Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record 

        Returns:
            List[MediaInfo] - info on all the media associated with the osti_id
        """
        response = requests.get(f'{self.target}media/{osti_id}',
                                headers = { "Authorization" : f"Bearer {self.token}" })
        
        Validation.handle_response(response)
        
        return self._convert_response_to_media_info(response)

    def get_media_content(self, media_file_id):
        """Obtain content stream of a particular MEDIA FILE by its unique ID

        Arguments:
            media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record

        Returns:
            Binary string that is the content associated with the media_file_id
        """
        response = requests.get(f"{self.target}media/file/{media_file_id}", 
                                headers={"Authorization": f"Bearer {self.token}"})

        Validation.handle_response(response)
        
        return response.content

    def post_media(self, osti_id, file_path=None, title=None, stream=False):
        """Attach the media found at the given filepath to the record associated
        with the given osti_id. 

        Optionally may include a "title" query parameter to set a title for the media.

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record

        Keyword Arguments:
            file_path -- filesystem path to upload and  associate with this metadata
            title -- optional "title" for media file
            stream -- optional ability to stream the given file, ideal for larger files
            
        Returns:
            MediaInfo 
        """
        query_params = ""
        parameters = {}

        """ 
        If optional parameters specified, these must be passed encoded. 

        Title is passed as an optional query parameter
        """
        if title is not None:
            parameters['title'] = title

        if(len(parameters) > 0):
            query_params = "?" + urlencode(parameters)
        
        if(stream):
            response = self.__post_media_stream(osti_id, file_path, query_params)
        else:
            response = self.__post_media_no_stream(osti_id, file_path, query_params)
            
        Validation.handle_response(response)

        return self._convert_response_to_media_info(response)
        
    def __post_media_stream(self, osti_id, file_path=None, query_params=None):
        """Attach the media found at the given filepath to the record associated
        with the given osti_id. 

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record

        Keyword Arguments:
            file_path -- filesystem path to upload and  associate with this metadata
            query_params -- optional includes "title" for media file
            
        Returns:
            MediaInfo 
        """
        # get a filename component from the path, or make a default
        filename = os.path.basename(file_path) or str(osti_id) + ".pdf"

        # if posting a FILE, send that; if not, send just the PARAMETERS
        if file_path is not None:
            if(file_path.startswith("http")):
                response = requests.get(file_path, stream=True)
                response.raw.decode_content = True
                
                mp_encoder = MultipartEncoder(
                    fields={'file': (filename, response.content, mimetypes.guess_type(filename)[0])}
                )
                response = requests.post(f'{self.target}media/{osti_id}{query_params}',
                            headers = { "Authorization" : f"Bearer {self.token}", "Content-Type": mp_encoder.content_type},
                            data=mp_encoder)
            else:
                with open(file_path, 'rb') as f:
                    m = MultipartEncoder(
                            fields={'file': (filename, f, mimetypes.guess_type(filename)[0] )}
                    )

                    response = requests.post(f'{self.target}media/{osti_id}{query_params}',
                            headers = { "Authorization" : f"Bearer {self.token}", 'Content-Type': m.content_type },
                            data=m)
        else:
            raise ValueError("File path is missing.")
            
        return response

    def __post_media_no_stream(self, osti_id, file_path=None, query_params=None):
        """Attach the media found at the given filepath to the record associated
        with the given osti_id. 

        Optionally may include a "title" query parameter to set a title for the media.

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record

        Keyword Arguments:
            file_path -- filesystem path to upload and  associate with this metadata
            query_params -- optional includes "title" for media file
            
        Returns:
            MediaInfo 
        """

        # if posting a FILE, send that; if not, send just the PARAMETERS
        if file_path is not None:
            if(file_path.startswith("http")):
                res = requests.get(file_path)
                filename = os.path.basename(file_path) or str(osti_id) + ".pdf"

                response = requests.post(f'{self.target}media/{osti_id}{query_params}',
                            headers = { "Authorization" : f"Bearer {self.token}"},
                            files={'file': (filename, res.content, mimetypes.guess_type(filename)[0])})
            else:
                response = requests.post(f'{self.target}media/{osti_id}{query_params}',
                        headers = { "Authorization" : f"Bearer {self.token}"},
                        files={ 'file': open(file_path, 'rb') })
        else:
            raise ValueError("File path is missing.")
            
        return response

    def put_media(self, osti_id, media_id, file_path=None, title=None, stream=False):
        """Replace a given media set with a new basis file.
        This will replace the previous media set. Both osti_id and media_id (of the set to replace) 
        are required.

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record

        Keyword Arguments:
            title -- optional "title" for media file
            file_path -- filesystem path to upload and  associate with this metadata
            stream -- optional ability to stream the given file, ideal for larger files
            
        Returns:
            MediaInfo 
        """
        query_params = ""
        parameters = {}

        """ 
        If optional parameters specified, these must be passed encoded. 

        Title is passed as an optional query parameter
        """
        if title is not None:
            parameters['title'] = title

        if(len(parameters) > 0):
            query_params = "?" + urlencode(parameters)
        
        if(stream):
            response = self.__put_media_stream(osti_id, media_id, file_path, query_params)
        else:
            response = self.__put_media_no_stream(osti_id, media_id, file_path, query_params)
            
        Validation.handle_response(response)

        return self._convert_response_to_media_info(response)
        
    def __put_media_stream(self, osti_id, media_id, file_path=None, query_params=None):
        """Replace a given media set with a new basis file.
        This will replace the previous media set. Intended for larger files

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record

        Keyword Arguments:
            file_path -- filesystem path to upload and  associate with this metadata
            query_params -- optional includes "title" for media file
            
        Returns:
            MediaInfo 
        """

        # get the base filename or presume one
        filename = os.path.basename(file_path) or str(osti_id) + ".pdf"

        # if posting a FILE, send that; if not, send just the PARAMETERS
        if file_path is not None:
            if(file_path.startswith("http")):
                response = requests.get(file_path, stream=True)
                response.raw.decode_content = True
                
                mp_encoder = MultipartEncoder(
                    fields={'file': (filename, response.content, mimetypes.guess_type(filename)[0])}
                )   
                response = requests.put(f'{self.target}media/{osti_id}/{media_id}{query_params}',
                            headers = { "Authorization" : f"Bearer {self.token}", "Content-Type": mp_encoder.content_type},
                            data=mp_encoder)
                
            else:
                with open(file_path, 'rb') as f:
                    m = MultipartEncoder(
                            fields={'file': (filename, f, mimetypes.guess_type(filename)[0] )}
                    )

                    response = requests.put(f'{self.target}media/{osti_id}/{media_id}{query_params}',
                            headers = { "Authorization" : f"Bearer {self.token}", 'Content-Type': m.content_type },
                            data=m)
        else:
            raise ValueError("File path is missing.")
            
        return response

    def __put_media_no_stream(self, osti_id, media_id, file_path=None, query_params=None):
        """Replace a given media set with a new basis file.
        This will replace the previous media set

        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record

        Keyword Arguments:
            file_path -- filesystem path to upload and  associate with this metadata
            query_params -- optional includes "title" for media file
            
        Returns:
            MediaInfo 
        """

        # if putting a FILE, send that; if not, send just the PARAMETERS
        if file_path is not None:
            if(file_path.startswith("http")):
                res = requests.get(file_path)
                filename = os.path.basename(file_path) or str(osti_id) + ".pdf"

                response = requests.put(f'{self.target}media/{osti_id}/{media_id}{query_params}',
                            headers = { "Authorization" : f"Bearer {self.token}"},
                            files={'file': (filename, res.content, mimetypes.guess_type(filename)[0]) })
            else:
                response = requests.put(f'{self.target}media/{osti_id}/{media_id}{query_params}',
                        headers = { "Authorization" : f"Bearer {self.token}"},
                        files={ 'file': open(file_path, 'rb') })
        else:
            raise ValueError("File path is missing.")
            
        return response
    
    def delete_record(self, osti_id:int, reason:str) -> None:
        """"
        Delete a given metadata record from the system by its OSTI ID
        
        Arguments:
            osti_id -- the ID to delete
            reason -- the stated reason for record deletion for history

        Raises:
            BadRequestException -- missing required reason value or unable to interpret OSTI ID value
            ForbiddenException -- user token does not have proper permission to remove record
            UnauthorizedException -- no user token provided
            NotFoundException -- record OSTI ID is not on file
            ServerException -- unknown service error occurred
        """

        response = requests.delete(f"{self.target}records/{osti_id}?reason={reason}",
                                   headers = { "Authorization" : f"Bearer {self.token}"})
        
        Validation.handle_response(response)


    def delete_single_media(self, osti_id, media_id, reason):
        """Disassociate an individual media set from this OSTI ID

        Arguments:
            osti_id -- ID that uniquely identifies an E-Link 2.0 Record
            media_id -- ID that uniquely identifies a media file associated with an E-Link 2.0 Record
            reason -- Reason for deleting all media

        Returns:
            int - the total number of rows removed
        """
        response = requests.delete(f"{self.target}media/{osti_id}/{media_id}?reason={reason}", headers={"Authorization": f"Bearer {self.token}"})

        Validation.handle_response(response)

        if(response.status_code == 204): 
            return int(response.headers['x-total-count'])

    def delete_all_media(self, osti_id, reason):
        """Disassociate ALL media sets from this OSTI ID 
        
        Arguments:
            osti_id -- ID that uniquely identifies an E-link 2.0 Record
            reason -- Reason for deleting all media

        Returns:
            int - the total number of rows removed
        """
        response = requests.delete(f"{self.target}media/{osti_id}?reason={reason}", headers={"Authorization": f"Bearer {self.token}"})

        Validation.handle_response(response)
        
        if(response.status_code == 204): 
            return int(response.headers['x-total-count'])
