from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator

class Identifier(BaseModel):
    """
    Different types of identifying numbers, including DOE contract numbers, report numbers, ISSN, ISBN, or other identifying numbers
    associated with the product or record.  Each element requires a "type" (enumerated by an Identifier.Type value) and the
    "value" of the identifier.
    """
    model_config = ConfigDict(validate_assignment=True)
    
    class Type(Enum):
        """
        Indicates the particular TYPE of this identifier.
        """
        AUTH_REVISION_NUMBER="AUTH_REV"
        AWARD_DOI="AWARD_DOI"
        DOE_CONTRACT_NUMBER="CN_DOE"
        CONTRACT_NUMBER="CN_NONDOE"
        CODEN="CODEN"
        DOE_DOCKET="DOE_DOCKET"
        EDB="EDB"
        ETDE_REFERENCE_NUMBER="ETDE_RN"
        INIS_REFERENCE_NUMBER="INIS_RN"
        ISBN="ISBN"
        ISSN="ISSN"
        LEGACY="LEGACY"
        NSA="NSA"
        OPENNET_ACCESSION_NUMBER="OPN_ACC"
        OTHER_IDENTIFIER="OTHER_ID"
        PATENT="PATENT"
        RD_PROJECT_IDENTIFIER="PROJ_ID"
        PROPOSAL_NUMBER="PROP_REV"
        REFERENCE_NUMBER="REF"
        REL_TRN="REL_TRN"
        REPORT_NUMBER="RN"
        TRN="TRN"
        TVI="TVI"
        USER_VERSION_NUMBER="USER_VER"
        WORK_AUTHORIZATION_NUMBER="WORK_AUTH"
        WORK_PROPOSAL_NUMBER="WORK_PROP"

        def __str__(self):
            return str(self.value)

    type:str
    value:str
    
    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in Identifier.Type]:
            raise ValueError("Unknown type value {}.".format(value))
        return value