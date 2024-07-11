from pydantic import BaseModel, ConfigDict, field_validator
import re

class Affiliation(BaseModel):
    """
    Data model for Person affiliations.
    
    may contain one or both of "name" or "ror_id" values.
    "ror_id" is validated against a given pattern for proper format according to ror.org specifications.
    """
    model_config = ConfigDict(validate_assignment=True)
    __ROR_ID_PATTERN = re.compile("^(?:(?:(http(s?):\/\/)?(?:ror\.org\/)))?(0[a-hj-km-np-tv-z|0-9]{6}[0-9]{2})$")

    name:str = None
    ror_id:str = None

    @field_validator("ror_id")
    @classmethod
    def validate_ror_id(cls, value: str) -> str:
        if value is not None and not cls.__ROR_ID_PATTERN.fullmatch(value):
            raise ValueError("Invalid ROR ID value.")
        return value