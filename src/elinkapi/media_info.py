from pydantic import BaseModel, ConfigDict
from typing import List
import datetime
from .media_file import MediaFile

class MediaInfo(BaseModel):
    """
    Information about an associated "media set" for this product.  A media set is defined as one or more
    files or URLs to full text, along with any derived content (such as OCR versions, text extracted from
    full text, cached URL contents, etc.) generated during media processing.

    Most fields are administrative, and set during processing.  An entire set is uniquely identified by
    its media_id, and will be also associated with the osti_id of the record to which it is attached.

    The status value generally will indicate its processing status; "C" indicates completed, "P" indicates
    in processing, "X" indicating a failure during media processing.

    See MediaFile class for additional information on individual files or URLs making up this media set.
    """
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
