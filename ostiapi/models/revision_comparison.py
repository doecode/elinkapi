from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from enum import Enum
import datetime

class DataPointer(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    pointer: str
    value: str

class Difference(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    pointer: str
    left: str
    right: str

class RevisionComparison(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    left_only: List[DataPointer] 
    right_only: List[DataPointer]
    differences: List[Difference]

