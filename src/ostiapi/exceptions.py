
HTTP_STATUS_CODES = {
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Resource Conflict",
    500: "Internal Service Error"
}

# Define some helpfully-named Exceptions for API issues
class APIException(Exception):
    """ Error or Exception handling a particular request. """

    # return/status code for this exception
    status_code: int = 500
    message: str = None

    def __init__(self, 
                 message: str = None, 
                 status_code: int = None)-> None:
        status_code = status_code or getattr(self.__class__, "status_code", None)
        if message is None:
            if self.message:
                message = self.message
            elif status_code:
                message = HTTP_STATUS_CODES.get(status_code, "")

        super().__init__(message)
        # set this exception's code
        self.status_code = status_code or self.status_code

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

class ValidationException(APIException):
    """Adds validation errors from the response to the exception message"""
    status_code = 400
    errors: list = []

    def __init__(self, errors: list = None)->None:

        super().__init__(self._message_from_details(errors))
        self.errors = errors

    def _message_from_details(self, errors: list) -> str:
        details = []

        for error in errors:
            details.append(error['detail'])
            
        return ", ".join(details)
        
class ConflictException(APIException):
    """ The url or file already exists on the server. """
    status_code = 409