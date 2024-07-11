from pydantic import BaseModel, ConfigDict, field_validator
from .utils import Validation

class Affiliation(BaseModel):
    """
    Data model for Person affiliations.
    
    may contain one or both of "name" or "ror_id" values.
    "ror_id" is validated against a given pattern for proper format according to ror.org specifications.
    """
    model_config = ConfigDict(validate_assignment=True)

    name:str = None
    ror_id:str = None

    @field_validator("ror_id")
    @classmethod
    def validate_ror_id(cls, value: str) -> str:
        Validation.find_ror_value(value)
        return value