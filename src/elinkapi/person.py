from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from .affiliation import Affiliation
from .contribution import Contribution

class Person(BaseModel):
    """
    Class representing a particular Person involved in production, maintenance, or distribution of this
    product.  This includes authors, contributors, contact information, releasing official, and others.

    Each Person has a defined Type (see Person.Type enumeration) to indicate the primary relation of this
    person to the record.  For CONTRIBUTING type, it is expected the contributor_type to detail the type of
    contribution this person provided, defined by contribution.Contribution enumeration.
    """
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        """
        Defines the primary "type" of this Person in relation to the record or product.  For CONTRIBUTING
        persons, the contributor_type is also expected.
        """
        AUTHOR="AUTHOR"
        CONTRIBUTING="CONTRIBUTING"
        CONTACT="CONTACT"
        PROTECTED_EMAIL="PROT_CE"
        PROTECTED_RELEASER="PROT_RO"
        RELEASE="RELEASE"
        BUSINESS_OFFICIAL="SBIZ_BO"
        PRINCIPAL_INVESTIGATOR="SBIZ_PI"
        
    type: str
    first_name: str = None
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
        if value not in [type.value for type in Contribution]:
            raise ValueError('Unknown contributor type value {}.'.format(value))
        return value
    
    def add_email(self, address: str):
        """
        Add a contact email to this person.
        """
        if self.email is None:
            self.email = []
        self.email.append(address)

    def add_affiliation(self, affiliation: Affiliation):
        """
        Add an affiliation to this Person.
        """
        if self.affiliations is None:
            self.affiliations = []
        self.affiliations.append(affiliation)

    