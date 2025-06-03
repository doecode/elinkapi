from pydantic import BaseModel
from typing import List
import datetime

class AuditLog(BaseModel):
    """
    Descriptive audit logging of processing states this record has
    undertaken during release.
    """
    # List of one or more messages relevant to this event
    messages: List[str]
    # usually SUCCESS or FAIL
    status: str
    # the worker or process involved; e.g., DOI, RELEASER, VALIDATOR, etc
    type: str
    # the date-time of the event
    audit_date: datetime.datetime