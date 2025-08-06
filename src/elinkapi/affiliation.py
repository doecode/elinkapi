from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from .utils import Validation
from typing import Optional

class Affiliation(BaseModel):
    """
    Data model for Person affiliations.
    
    may contain one or both of "name" or "ror_id" values.
    "ror_id" is validated against a given pattern for proper format according to ror.org specifications.
    """
    model_config = ConfigDict(validate_assignment=True)

    name:Optional[str] = None
    ror_id:Optional[str] = None

    @model_validator(mode = 'after')
    def name_or_ror(self):
        if not self.name and not self.ror_id:
            raise ValueError("Either name and/or ROR ID value is required.")
        return self

    @field_validator("ror_id")
    @classmethod
    def validate_ror_id(cls, value: str) -> str:
        if value: 
            Validation.find_ror_value(value)
        return value