import re
from .exceptions import NotFoundException,ForbiddenException,UnauthorizedException,ServerException,ConflictException,BadRequestException

class Validation:
    _ROR_ID_PATTERN = re.compile("^(?:(?:(http(s?):\/\/)?(?:ror\.org\/)))?(0[a-hj-km-np-tv-z|0-9]{6}[0-9]{2})$")

    @classmethod
    def find_ror_value(cls, value:str) -> str:
        """
        Attempt to match against valid ROR ID patterns.  If matched, return
        the ROR ID value only.
        """
        match = cls._ROR_ID_PATTERN.search(value)
        if match is None:
            raise ValueError("Invalid ROR ID value.")
        
        return match.group(1)
    
    @classmethod
    def handle_response(self, response):
        """Evaluates the response and selects the appropriate action based on 
        the status code 

        Arguments:
            response -- response from E-Link 2.0

        Raises:
            UnauthorizedException: API token not provided with request
            ForbiddenException: User is not allowed to access
            NotFoundException: Requested object could not be found
            ConflictException: Resource already exists
            BadRequestException: Issue with the submitted json, see error message for details
            ServerException: Unknown error

        Returns:
            Either the successful response or the appropriate exception is raised
        """
        if response.status_code in [200, 201, 204]:
            return response
        elif response.status_code == 400:
            raise BadRequestException(response.text)
        elif response.status_code == 401:
            raise UnauthorizedException('No user account information supplied.')
        elif response.status_code == 403:
            raise ForbiddenException(response.text)
        elif response.status_code == 404:
            raise NotFoundException(response.text)
        elif response.status_code == 409:
            raise ConflictException("Conflict, URL or file is already associated with this record.")
        else: # 500
            raise ServerException('ELINK service is not available or unknown connection error.')
