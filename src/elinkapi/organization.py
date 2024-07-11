from enum import Enum
from .identifier import Identifier
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from .utils import Validation

class Organization(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        AUTHOR="AUTHOR"
        CONTRIBUTING="CONTRIBUTING"
        RESEARCHING="RESEARCHING"
        SPONSOR="SPONSOR"
        PAMS_TD_INST="PAMS_TD_INST"

    class Contribution(Enum):
        DataCollector="DataCollector"
        DataCurator="DataCurator"
        DataManager="DataManager"
        Distributor="Distributor"
        Editor="Editor"
        HostingInstitution="HostingInstitution"
        Producer="Producer"
        ProjectLeader="ProjectLeader"
        ProjectManager="ProjectManager"
        ProjectMember="ProjectMember"
        RegistrationAgency="RegistrationAgency"
        RegistrationAuthority="RegistrationAuthority"
        Researcher="Researcher"
        ResearchGroup="ResearchGroup"
        RightsHolder="RightsHolder"
        Sponsor="Sponsor"
        Supervisor="Supervisor"
        WorkfPackageLeader="WorkPackageLeader"
        Other="Other"

    type:str
    name:str
    contributor_type: str = None
    identifiers: List[Identifier] = None
    ror_id:str = None

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in cls.Type]:
            raise ValueError("Unknown type value {}.".format(value))
        return value
    
    @field_validator("contributor_type")
    @classmethod
    def contributor_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in cls.Contribution]:
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
        if self.identifiers is None:
            self.identifiers=[]
        self.identifiers.append(item)
    
