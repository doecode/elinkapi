from .record import RecordResponse
from .utils import Validation
import json
import requests

class Query:
    """
    Search/query object.  Contains total count of records found,
    the data (List of Record objects), and links to next and/or previous
    pages as applicable.

    Query is iterative, so may use "data" element a page at a time, or
    freely iterate until all rows are obtained, as the Query will automatically
    handle pagination forward.

    .. code-block:: python
        query = api.query_records(title='Science report', product_type = 'TR')
        
        for record in query:
            print (record.model_dump_json(exclude_none=True))
    """
    total_rows: int
    next_url: str 
    previous_url: str
    first_url: str
    data: list[RecordResponse]
    _target: str
    _token: str
    
    def _response_to_records(self, response):
        """Returns array of Records"""
        json_records = json.loads(response.text)
        
        if(not isinstance(json_records, list)):
            json_records = [json_records]
        records = [RecordResponse(**record) for record in json_records]
        
        return records
    
    def _load(self, response):
        """ load up information from the response object."""
        self.total_rows = int(response.headers['x-total-count'] if 'x-total-count' in response.headers else 0)
        # strip servlet path from these for target link later
        self.first_url = response.links['first']['url'].replace("/elink2api/", "") if 'first' in response.links else ""
        self.next_url = response.links['next']['url'].replace('/elink2api/', '') if 'next' in response.links else ''
        self.previous_url = response.links['prev']['url'].replace('/elink2api/', '') if 'prev' in response.links else ''
        self.data = self._response_to_records(response)

    def total_count(self) -> int:
        return self.total_rows
    
    def data(self):
        return self.data

    def __init__(self, response, target=None, token=None):
        """
        Set up the object based on a given HTTP service response.
        """
        self._load(response)
        self._target = target
        self._token = token

    def has_next(self):
        return self.next_url != ''
    
    def has_previous(self):
        return self.previous_url != ''
    
    def __iter__(self):
        return self
    
    def next(self):
        return self.__next__()
    
    def previous(self):
        if self.has_previous():
            response = requests.get(f"{self._target}{self.previous_url}",
                                    headers = { "Authorization" : f"Bearer {self._token}"})
            Validation.handle_response(response)
            self._load(response)
            return self
        else:
            raise StopIteration
    
    def reset(self):
        """
        Restarts the query object from first page of results if possible.  If no valid first page,
        raise StopIteration.
        """
        if self.first_url:
            response = requests.get(f"{self._target}{self.first_url}",
                                    headers = { "Authorization" : f"Bearer {self._token}"})
            Validation.handle_response(response)
            self._load(response)
        else:
            raise StopIteration


    def __next__(self) -> RecordResponse:
        """
        Return the next record in this Query, if available.
        Once this runs out of pages with results, it will raise StopIteration.
        """
        try:
            record = self.data.pop()

            return record
        except IndexError:
            # if we have a next page, try that
            if self.has_next():
                # get the next set
                response = requests.get(f"{self._target}{self.next_url}",
                                        headers = { "Authorization" : f"Bearer {self._token}"})
                Validation.handle_response(response)
                self._load(response)
                return self.__next__()
            else:
                raise StopIteration