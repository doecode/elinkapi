from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from .affiliation import Affiliation

class Person(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        AUTHOR="AUTHOR"
        CONTRIBUTING="CONTRIBUTING"
        CONTACT="CONTACT"
        PROTECTED_EMAIL="PROT_CE"
        PROTECTED_RELEASER="PROT_RO"
        RELEASE="RELEASE"
        BUSINESS_OFFICIAL="SBIZ_BO"
        PRINCIPAL_INVESTIGATOR="SBIZ_PI"
    class Contribution(Enum):
        DataCollector="DataCollector"
        DataCurator="DataCurator"
        DataManager="DataManager"
        Distributor="Distributor"
        Editor="Editor"
        Producer="Producer"
        ProjectLeader="ProjectLeader"
        ProjectManager="ProjectManager"
        ProjectMember="ProjectMember"
        RelatedPerson="RelatedPerson"
        Researcher="Researcher"
        RightsHolder="RightsHolder"
        Supervisor="Supervisor"
        WorkfPackageLeader="WorkPackageLeader"
        Other="Other"

    type: str
    first_name: str
    middle_name: str = None
    last_name: str
    orcid: str = None
    phone: str = None
    email: List[str] = None
    affiliations: List[Affiliation] = None
    contributor_type: str = None

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, value) -> str:
        if value not in [type.value for type in cls.Type]:
            raise ValueError('Unknown type value {}.'.format(value))
        return value

    @field_validator("contributor_type")
    @classmethod
    def contributor_must_be_valid(cls, value) -> str:
        if value not in [type.value for type in cls.Contribution]:
            raise ValueError('Unknown contributor type value {}.'.format(value))
        return value
    
    def add_email(self, address: str):
        if self.email is None:
            self.email = []
        self.email.append(address)

    """
    Add an affiliation to this Person.
    """
    def add_affiliation(self, affiliation: Affiliation):
        if self.affiliations is None:
            self.affiliations = []
        self.affiliations.append(affiliation)

    