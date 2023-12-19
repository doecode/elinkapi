from pydantic import BaseModel, ConfigDict
from error import Error
from typing import List

class ErrorResponse(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    errors: List[Error]