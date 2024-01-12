# OSTIAPI - A Python Interface for E-Link 2.0

## Open Questions
- Still need a license designation
- Do we want organizational credentials for Pypi test and/or Prod?
- see about enum for query to elink -- enum doesn't really make a ton of sense. Maybe prepopulated empty dict, would have to look and remove all empty values before urlencode. 

## Table of Contents
- [OSTIAPI - A Python Interface for E-Link 2.0](#ostiapi---a-python-interface-for-e-link-20)
  - [Open Questions](#open-questions)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Examples](#examples)
      - [Creating a New Record](#creating-a-new-record)
      - [Seeing Validation Errors on Exception](#seeing-validation-errors-on-exception)
      - [View Revision History](#view-revision-history)
      - [Adding Media to Record](#adding-media-to-record)
      - [Removing Media from a Record](#removing-media-from-a-record)
      - [Compare Two Revision Histories](#compare-two-revision-histories)
  - [Method Documentation](#method-documentation)
    - [Configuration](#configuration)
    - [Records](#records)
      - [Revisions](#revisions)
    - [Media](#media)
  - [Classes](#classes)
    - [Record](#record)
    - [Organization](#organization)
    - [Person](#person)
    - [Identifier](#identifier)
    - [Related Identifier](#related-identifier)
    - [Geolocation](#geolocation)
    - [Media Info](#media-info)
    - [Media File](#media-file)
    - [Revision](#revision)
    - [Revision Comparison](#revision-comparison)

## Introduction
This module is setup to mimic the E-Link 2.0 API Endpoints (API documentation found [here](https://review.osti.gov/elink2api/)) and allows for you to quickly get up and running submitting Records using Python. 

### Examples

#### Creating a New Record
```python
from ostiapi import ostiapi
from ostiapi.record import Record

ostiapi.set_api_token("___Your-API-Token___")
ostiapi.set_target_url('https://dev.osti.gov/elink2api/')

# Record with minimal fields to save
my_record_json = {
        "title": "A Dissertation Title",
        "site_ownership_code": "AAAA",
        "product_type": "TD"
        }
# Convert json to Record object
my_record = Record(**my_record_json)

saved_record = None
try:
    saved_record = ostiapi.post_new_record(my_record, "save")
except Exception as e:
    # Handle the exception as needed
```

#### Seeing Validation Errors on Exception
```python
from ostiapi import ostiapi
from ostiapi.record import Record

ostiapi.set_api_token("___Your-API-Token___")
ostiapi.set_target_url('https://review.osti.gov/elink2api/')

# Record missing fields, will give 2 validation errors, one for 
# each missing field: title and product_type
my_invalid_record_json = {
    "site_ownership_code": "AAAA"
}

try:
    # The pydantic model will raise exceptions for the 2 missing 
    # fields - title and product_type
    my_record = Record(**my_invalid_record_json)
except Exception as e:
    print('Exception on Record creation')

my_invalid_record_json = {
    "title": "A Sample Title",
    "product_type": "TD",
    "site_ownership_code": "AAAA"
}

saved_record = None
try:
    # The API will now return an error code on this call
    # because "AAAA" is not a valid site_ownership_code
    saved_record = ostiapi.post_new_record(my_record, "save")
except Exception as e:
    # Handle the exception as needed
```

#### View Revision History
```python
from ostiapi import ostiapi

ostiapi.set_api_token("___Your-API-Token___")

osti_id = 99999999

revision_history = None
try:
    revision_history = ostiapi.get_all_revisions(osti_id)
except Exception as e:
    // Handle the exception as needed

most_recent_revision = revision_history[0]
oldest_revision = revision_history[-1]
```

#### Adding Media to Record
```python
from ostiapi import ostiapi

ostiapi.set_api_token("___Your-API-Token___")

osti_id = 9999999
path_to_my_media = "/home/path/to/media.pdf"

saved_media = None
try:
    saved_media = ostiapi.post_media(osti_id, path_to_my_media)
except Exception as e:
    // Handle the exception as needed
```

#### Removing Media from a Record
```python
from ostiapi import ostiapi

ostiapi.set_api_token("___Your-API-Token___")

osti_id = 9999999
media_id = 71
reason = "Uploaded the wrong file"

response = None
try:
    response = ostiapi.delete_single_media(osti_id, media_id, reason)
except Exception as e:
    # Handle the exception as needed
```

#### Compare Two Revision Histories
```python
from ostiapi import ostiapi

ostiapi.set_api_token("___Your-API-Token___")

osti_id = 2300069
revision_id_left = 1
revision_id_right = 2

response = None
try:
    response = ostiapi.compare_two_revisions(osti_id, revision_id_left, revision_id_right)
except Exception as e:
    # // Handle the exception as needed
```


## Method Documentation

### Configuration
Method: 
> set_api_token(*api_token*)

Returns: The API token that has been set

Params: 
- *api_token* - **str**: Unique to user API token that can be generated from your E-Link 2.0 Account page
---
Method: 
> set_target_url(*url*="https://review.osti.gov/elink2api"):

Returns: The url that has been set

Params: 
- *url* - **str**: The url to which all other module methods will direct their requests (default: {"https://review.osti.gov/elink2api"})
---
### Records
Method:
>  get_single_record(*osti_id*)

Returns: Record

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
---
Method:
>  query_records(*params*)

Returns: List[Records]

Params:
- *params* - **dict**: See [here](https://review.osti.gov/elink2api/#tag/records/operation/getRecords) for 
    the list of allowed query parameters.
---
Method:
>  reserve_doi(*record*)

Returns: Record

Params: 
- *record* - **Record**: Metadata record that you wish to save to E-Link 2.0
---
Method:
>  post_new_record(record, *state*="save")

Returns: Record

Params:
- *record* - **Record**: Metadata record that you wish to send ("save" or "submit") to E-Link 2.0
- *state* - **str**: The desired submission *state* of the record ("save" or "submit")  (default: {"save"})
---
Method:
>  update_record(*osti_id*, *record*, *state*="save")

Returns: Record

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *record* - **Record**: Metadata record that you wish to make the new revision of OSTI ID
- *state* - **str**: The desired submission *state* of the record ("save" or "submit")  (default: {"save"})
---
#### Revisions
Method:
>  get_revision_by_number(*osti_id*, *revision_number*)

Returns: Record

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *revision_number* - **int**: The specific revision number to retrieve (original record is 1 and each revision increments upward by 1)
---
Method:
>  get_revision_by_date(*osti_id*, *date*)

Returns: Record

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *date* - **datetime**: Date on which you wish to search for a revision of a Record
---
Method:
>  get_all_revisions(*osti_id*)

Returns: RevisionHistory

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
---
Method:
> compare_two_revisions(osti_id, left, right)

Returns: List[RevisionComparison]

Params: 
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *left* - **int**: The first revision number to retrieve and compare to the right
- *right* - **int** The second revision number to retrieve and compare to the left
---
### Media
Method:
>  get_media(*osti_id*)

Returns: MediaInfo

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
---
Method:
>  get_media_content(*media_file_id*)

Returns: Byte string of the media file content

Params:
- *media_file_id* - **int**: ID that uniquely identifies a media file associated with an E-Link 2.0 Record
---
Method:
>  post_media(*osti_id*, *file_path*, *params*=None)

Returns: MediaInfo

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *file_path* - **str**: Path to the media file that will be attached to the Record 
- *params* - **dict**: "title" that can be associated with the media file
        "url" that points to media if not sending file (default; {None})
---
Method:
>  put_media(*osti_id*, *media_id*, *file_path*, *params*=None)

Returns: MediaInfo

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *media_id* - **int**: ID that uniquely identifies a media file associated with an E-Link 2.0 Record
- *file_path* - **str**: Path to the media file that will replace *media_id* Media
- *params* - **dict**: "title" that can be associated with the media file
        "url" that points to media if not sending file (default; {None}) 
---
Method:
>  delete_all_media(*osti_id*, *reason*)

Returns: True on success, False on failure

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *reason* - **str**: *reason* for deleting all media 
---
Method:
>  delete_single_media(*osti_id*, *media_id*, *reason*)

Returns: True on success, False on failure

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
- *media_id* - **int**: ID that uniquely identifies a media file associated with an E-Link 2.0 Record
- *reason* - **str**: reason for deleting media
---
## Classes
Each class is a pydantic model that validates the metadata's data types and 
enumerated values on instantiation of the class.

### Record
Matches the [Metadata model](https://review.osti.gov/elink2api/#tag/record_model) described in E-Link 2.0's API documentation

### Organization
Matches the [Organizations model](https://review.osti.gov/elink2api/#tag/organization_model) described in E-Link 2.0's API documentation

### Person
Matches the [Persons model](https://review.osti.gov/elink2api/#tag/person_model) described in E-Link 2.0's API documentation

### Identifier
Matches the [Identifiers model](https://review.osti.gov/elink2api/#tag/identifier_model) described in E-Link 2.0's API documentation

### Related Identifier
Matches the [Related Identifiers model](https://review.osti.gov/elink2api/#tag/related_identifier_model) described in E-Link 2.0's API documentation

### Geolocation
<u>Schema</u>
```python
Geolocation: {
    "type": str
    "label": str
    "points": List[Point]
}
Point: {
    "latitude": float
    "longitude": float
}
```
<u>Example</u>
```python
{
    "type": "BOX",
    "label": "Utah FORGE",
    "points": [
        {
            "latitude": 38.5148,
            "longitude": -112.879748
        },
        {
            "latitude": 38.483935,
            "longitude": 112.916367
        }
    ]
}
```

### Media Info
<u>Schema</u>
```python
[
    {
        "media_id": int,
        "revision": int,
        "access_limitations": List[str],
        "osti_id": int,
        "status": str,
        "added_by": int,
        "document_page_count": int,
        "mime_type": str,
        "media_title": str,
        "media_location": str,
        "media_source": str,
        "date_added": datetime,
        "date_updated": datetime,
        "date_valid_start": datetime,
        "date_valid_end": datetime,
        "files": List[MediaFile]
    }
]
```
<u>Example</u>
```python
[
    {
        "media_id": 233743,
        "revision": 3,
        "access_limitations": [],
        "osti_id": 99238,
        "status": "P",
        "added_by": 34582,
        "document_page_count": 23,
        "mime_type": "application/pdf",
        "media_title": "PDF of technical report content",
        "media_location": "L",
        "media_source": "MEDIA_API_UPLOAD",
        "date_added": "1992-03-08T11:23:44.123+00:00",
        "date_updated": "2009-11-05T08:33:12.231+00:00",
        "date_valid_start": "2021-02-13T16:32:23.234+00:00",
        "date_valid_end": "2021-02-15T12:32:11.332+00:00",
        "files": []
    }
]

```

### Media File
<u>Schema</u>
```python
{
    "media_file_id": int,
    "media_id": int,
    "revision": int,
    "status": str,
    "media_type": str,
    "url_type": str,
    "added_by_user_id": int,
    "file_size_bytes": int,
    "date_file_added": datetime,
    "date_file_updated": datetime"
}
```
<u>**Example**</u>
```python
{
    "media_file_id": 12001019,
    "media_id": 1900094,
    "revision": 2,
    "status": "ADDED",
    "media_type": "O",
    "url_type": "L",
    "added_by_user_id": 112293,
    "file_size_bytes": 159921,
    "date_file_added": "2023-12-20T22:13:16.668+00:00",
    "date_file_updated": "2023-12-20T22:13:16.668+00:00"
}
```

### Revision
<u>**Schema**</u>
```python
{
    "date_valid_start": datetime,
    "date_valid_end": datetime,
    "osti_id": int,
    "revision": int,
    "workflow_status": str
}
```
<u>**Example**</u>
```python
{
    "date_valid_start": "2022-12-04T13:22:45.092+00:00",
    "date_valid_end": "2023-12-04T13:22:45.092+00:00",
    "osti_id": 2302081,
    "revision": 2,
    "workflow_status": "R"
}
```

### Revision Comparison
<u>**Schema**</u>
```python
[
    {
        "date_valid_start": datetime,
        "date_valid_end": datetime,
        "osti_id": int,
        "revision": int,
        "workflow_status": str
    }
]
```
<u>**Example**</u>
```python
[
    {
        "pointer": "/edit_reason",
        "left": "API record creation",
        "right": "API metadata Update"
    },
    {
        "pointer": "/description",
        "left": "A custom description. Search on 'Allo-ballo holla olah'.",
        "right": "A NEW custom description. Search on 'Allo-ballo holla olah'."
    }
]
'```
