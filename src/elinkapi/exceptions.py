
import json

HTTP_STATUS_CODES = {
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Resource Conflict",
    500: "Internal Service Error"
}

class Error():
    """
    Detailed error message with source from Exceptions. Mostly used for
    interpreting BadRequestException cases of validation errors with submissions.
    """
    status: int = None
    detail: str = None
    source: str = None
    meta: str = None

    def __init__(self, status: int = None, detail: str = None, source: str = None, meta: str = None):
        self.status = status
        self.detail = detail
        self.source = source
        self.meta = meta

    def get_status(self) -> int:
        return self.status
    def get_detail(self) -> str:
        return self.detail
    def get_source(self) -> str:
        return self.source
    def get_meta(self) -> str:
        return self.meta
    
    def __repr__(self) -> str:
        return f'message: {self.detail} source: {self.source}'
    
    def __str__(self) -> str:
        return f'message: {self.detail} source: {self.source}'

# Define some helpfully-named Exceptions for API issues
class APIException(Exception):
    """ Error or Exception handling a particular request. """

    # return/status code for this exception
    status_code: int = 500
    message: str = None
    errors: list[Error] = []

    def __init__(self,
                 text: str) -> None:
        """
        Attempt to parse the text string for JSON response; if unable,
        take the message verbatim.
        """
        # default a message from the status code if present
        if text is None and self.status_code:
            self.message = HTTP_STATUS_CODES.get(status_code, "")
        else:
            # try to make a JSON and get details from there
            try:
                json_response = json.loads(text)

                # ensure the JSON response contains "errors"; if not, simple bad request
                if isinstance(json_response, dict) and 'errors' in json_response:
                    details = []

                    for error in json_response['errors']:
                        details.append(error['detail'])
                        self.errors.append(Error(**error))
                    # message is in the details
                    self.message = ", ".join(details)
                else:
                    # just take the text and go
                    self.message = text
            except json.JSONDecodeError as error:
                # give up and use the response as-is
                super().__init__(text)

    def get_errors(self) -> list[Error]:
        return self.errors

class NotFoundException(APIException):
    """ Record not on file. """
    status_code = 404
 
class ForbiddenException(APIException):
    """ Access was forbidden. """
    status_code = 403

class ServerException(APIException):
    """ Unknown internal server error. """
    status_code = 500

class UnauthorizedException(APIException):
    """ Unauthorized access attempted. """
    status_code = 401

class BadRequestException(APIException):
    """ Unable to parse the JSON Request made. """
    status_code = 400
        
class ConflictException(APIException):
    """ The url or file already exists on the server. """
    status_code = 409