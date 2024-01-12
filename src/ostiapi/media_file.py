from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from enum import Enum
import datetime

class MediaFile(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class UrlType(Enum):
        LOCALLY_HOSTED="L"
        OFFSITE_URL="O"

    media_file_id: int = None
    media_id: int = None
    revision: int = None
    parent_media_file_id: int = None
    status: str = None
    media_type: str = None
    url_type: str = None
    url: str = None
    added_by: int = None
    document_page_count: int = None
    file_size_bytes: int = None
    duration_seconds: int = None
    subtitle_tracks: int = None
    video_tracks: int = None
    mime_type: str = None
    media_source: str = None
    date_file_added: datetime.datetime = None
    date_file_updated: datetime.datetime = None

    @field_validator("url_type")
    @classmethod
    def url_type_must_be_valid(cls, value: str) -> str:
        if value not in [type.value for type in cls.UrlType]:
            raise ValueError("Unknown URL type {}.".format(value))
        return value