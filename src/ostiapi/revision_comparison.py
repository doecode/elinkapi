from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

class RevisionComparison(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    pointer: str
    left: str
    right: str