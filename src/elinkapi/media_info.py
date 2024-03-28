from pydantic import BaseModel, ConfigDict
from typing import List
import datetime
from .media_file import MediaFile

class MediaInfo(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    media_id: int = None
    revision: int = None
    osti_id: int = None
    status: str  = None
    added_by: int = None
    document_page_count: int = None
    mime_type: str = None
    media_title: str = None
    media_location: str = None
    media_source: str = None
    date_added: datetime.datetime = None
    date_updated: datetime.datetime = None
    date_valid_start: datetime.datetime = None
    date_valid_end: datetime.datetime = None
    files: List[MediaFile] = None
