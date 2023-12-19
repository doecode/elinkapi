from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

class Error(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    status: int
    title: str = None
    detail: str
    source: dict[str, str]
    meta: dict[str, str] = None
