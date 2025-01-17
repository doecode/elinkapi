from enum import Enum
from .identifier import Identifier
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import List
from .utils import Validation
from .contribution import Contribution

class Organization(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        AUTHOR="AUTHOR"
        CONTRIBUTING="CONTRIBUTING"
        RESEARCHING="RESEARCHING"
        SPONSOR="SPONSOR"
        PAMS_TD_INST="PAMS_TD_INST"

    type:str
    name:str = None
    contributor_type: str = None
    identifiers: List[Identifier] = None
    ror_id:str = None

    @model_validator(mode = 'after')
    def name_or_ror(self):
        if not self.name and not self.ror_id:
            raise ValueError("Either name and/or ROR ID value is required.")
        return self

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in cls.Type]:
            raise ValueError("Unknown type value {}.".format(value))
        return value
    
    @field_validator("contributor_type")
    @classmethod
    def contributor_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in Contribution]:
            raise ValueError("Unknown contribution type {}.".format(value))
        return value

    def _add_identifier(self, identifier):
        self.identifiers.append(identifier)

    
    @field_validator("ror_id")
    @classmethod
    def validate_ror_id(cls, value: str) -> str:
        if value is not None:
            Validation.find_ror_value(value)
        return value


    """
    Add an identifier to this Organization.
    """
    def add(self, item: Identifier):
        if self.type is not None and self.type != Organization.Type.SPONSOR.value:
            raise ValueError ("Only sponsoring organizations may specify identifiers.")
        
        if item.type not in [Identifier.Type.AWARD_DOI.value, Identifier.Type.CONTRACT_NUMBER.value, Identifier.Type.DOE_CONTRACT_NUMBER.value]:
            raise ValueError ("Identifier type not allowed as Organization identifier.")
        
        if self.identifiers is None:
            self.identifiers=[]
        self.identifiers.append(item)
    
