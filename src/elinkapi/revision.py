from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from enum import Enum
import datetime

class Revision(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    osti_id: int 
    revision: int
    date_valid_start: datetime.datetime
    date_valid_end: datetime.datetime = None
    workflow_status: str

    @field_validator("workflow_status")
    @classmethod
    def workflow_status_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in cls.WorkflowStatus]:
            raise ValueError("Unknown Workflow Status {}.".format(value))
        return value
