from pydantic import BaseModel
from typing import List
import datetime

class AuditLog(BaseModel):
    """
    Descriptive audit logging of processing states this record has
    undertaken during release.

    Indicates back-end processing of a given Record, generally with
    a list of one or more informative messages, a status value of
    SUCCESS or FAIL for the operation, and the worker (type) 
    performing this processing (DOI, RELEASER, etc.)
    """
    # List of one or more messages relevant to this event
    messages: List[str]
    # usually SUCCESS or FAIL
    status: str
    # the worker or process involved; e.g., DOI, RELEASER, VALIDATOR, etc
    type: str
    # the date-time of the event
    audit_date: datetime.datetime