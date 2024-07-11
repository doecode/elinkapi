# ELINKAPI - A Python Interface for E-Link 2.0<a id="elinkapi---a-python-interface-for-e-link-20"></a>

## Table of Contents<a id="table-of-contents"></a>
- [ELINKAPI - A Python Interface for E-Link 2.0](#elinkapi---a-python-interface-for-e-link-20)
  - [Open Questions](#open-questions)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
      - [Importing the Package from test.pypi.org](#importing-the-package-from-testpypiorg)
      - [Importing the Package from Production PyPI](#importing-the-package-from-production-pypi)
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
  - [Exceptions](#exceptions)
    - [UnauthorizedException](#unauthorized-exception)
    - [ForbiddenException](#forbidden-exception)
    - [BadRequestException](#bad-request-exception)
    - [NotFoundException](#not-found-exception)
    - [ConflictException](#conflict-exception)
    - [ValidationException](#validation-exception)
    - [ServerException](#server-exception)

## Introduction<a id="introduction"></a>
This module is setup to mimic the E-Link 2.0 API Endpoints (API documentation found [here](https://review.osti.gov/elink2api/)) and allows for you to quickly get up and running submitting Records using Python. 

## Installation<a id="installation"></a>

#### Importing the Package from test.pypi.org<a id="importing-the-package-from-testpypiorg"></a>
1. Install the package, but don't grab the dependencies (pip will attempt to grab everything from the test server, which we do not want): `pip install --index-url https://test.pypi.org/simple/ --no-deps elinkapi`
2. Now install the other dependencies: `pip install elinkapi`
3. Or install them separately: `pip install requests pydantic urllib3==1.26.6`
4. Access the E-Link connector via `from elinkapi import Elink` and creating an instance for use with your API key: `api = Elink(token="Your_API_Token")`
5. API classes are accessible using `from elinkapi import Record`, etc.
6. Exception classes generated by the API are accessible using `from elinkapi import exceptions` then catching appropriate `exceptions.ValidationException` and the like.

#### Importing the Package from Production PyPI<a id="importing-the-package-from-production-pypi"></a>
1. Install the package: `pip install elinkapi`
2. Access the E-Link connector via `from elinkapi import Elink` and creating an instance for use with your API key: `api = Elink(token="Your_API_Token")`
3. API classes are accessible using `from elinkapi import Record`, etc.
4. Exception classes generated by the API are accessible using `from elinkapi import exceptions` then catching appropriate `exceptions.ValidationException` and the like.

## Examples<a id="examples"></a>

#### Creating a New Record<a id="creating-a-new-record"></a>
Note: Ensure site_ownership_code is a value to which your user account token has sufficient access to create records.
```python
from elinkapi import Elink, Record, exceptions

api = Elink(token="__Your_API_Token__")

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
    saved_record = api.post_new_record(my_record, "save")
except exceptions.ValidationException as ve:
    # ve.message = "Site Code AAAA is not valid."
    # ve.errors provides more details:
    # [{"status":"400", "detail":"Site Code AAAA is not valid.", "source":{"pointer":"site_ownership_code"}}]
```

#### Seeing Validation Errors on Exception<a id="seeing-validation-errors-on-exception"></a>
```python
from elinkapi import Elink, Record, ValidationException

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
    # pydantic will return "missing" required fields as below:
    # 2 validation errors for Record
    # product_type
    #    Field required [type=missing, input_value={'site_ownership_code': 'BBBB'}, input_type=dict]
    #    For further information visit https://errors.pydantic.dev/2.6/v/missing
    # title
    #    Field required [type=missing, input_value={'site_ownership_code': 'BBBB'}, input_type=dict]
    #    For further information visit https://errors.pydantic.dev/2.6/v/missing

my_invalid_record_json = {
    "title": "A Sample Title",
    "product_type": "TD",
    "site_ownership_code": "AAAA"
}

my_record = Record(**my_invalid_record_json)

saved_record = None
try:
    # The API will now return an error code on this call
    # because "AAAA" is not a valid site_ownership_code
    saved_record = api.post_new_record(my_record, "save")
except exceptions.ValidationException as ve:
    # E-Link ValidationException provides details of the API response:
    # ve.message = "Site Code AAAA is not valid."
    # ve.errors provides more details:
    # [{"status":"400", "detail":"Site Code AAAA is not valid.", "source":{"pointer":"site_ownership_code"}}]
```

#### View Revision History<a id="view-revision-history"></a>
```python
from elinkapi import Elink

api = Elink(token="__Your_API_Token__")

osti_id = 99999999

revision_history = None
try:
    revision_history = api.get_all_revisions(osti_id)
except Exception as e:
    # Handle the exception as needed

most_recent_revision = revision_history[0]
oldest_revision = revision_history[-1]
```

#### Adding Media to Record<a id="adding-media-to-record"></a>
```python
from elinkapi import Elink

api = Elink(token = '__Your_API_Token__')

osti_id = 9999999
path_to_my_media = "/home/path/to/media.pdf"

saved_media = None
try:
    saved_media = api.post_media(osti_id, path_to_my_media)
except Exception as e:
    # Handle the exception as needed
```

#### Removing Media from a Record<a id="removing-media-from-a-record"></a>
```python
from elinkapi import Elink

api = Elink(token = "___Your-API-Token___")

osti_id = 9999999
media_id = 71
reason = "Uploaded the wrong file"

response = None
try:
    response = api.delete_single_media(osti_id, media_id, reason)
except Exception as e:
    # Handle the exception as needed
```

#### Compare Two Revision Histories<a id="compare-two-revision-histories"></a>
```python
from elinkapi import Elink

api = Elink(token = "___Your-API-Token___")

osti_id = 2300069
revision_id_left = 1
revision_id_right = 2

response = None
try:
    response = elinkapi.compare_two_revisions(osti_id, revision_id_left, revision_id_right)
except Exception as e:
    # Handle the exception as needed
```


## Method Documentation<a id="method-documentation"></a>

### Configuration<a id="configuration"></a>

The following methods may alter parameters on existing Elink instances to alter or set values.

```python
from elinkapi import Elink

# you may set these directly or alter them later
# note target defaults to "https://review.osti.gov/elink2api/" for the E-Link 2.0 Beta
api = Elink(token = 'TOKENVALUE', target='API_ENDPOINT')

# change them
api.set_api_token("NEWTOKEN")
api.set_target_url("NEW_API_ENDPOINT")

```
Method: 
> set_api_token(*api_token*)

Returns: None

Params: 
- *api_token* - **str**: Unique to user API token that can be generated from your E-Link 2.0 Account page
---
Method: 
> set_target_url(*url*="https://review.osti.gov/elink2api"):

Returns: None

Params: 
- *url* - **str**: The url to which all other module methods will direct their requests (default: {"https://review.osti.gov/elink2api"})
---
### Records<a id="records"></a>
Method:
>  get_single_record(*osti_id*)

Returns: Record

Params:
- *osti_id* - **int**: ID that uniquely identifies an E-Link 2.0 Record
---
Method:
>  query_records(*params*)

Example:
```python
api.query_records(title="science")
```

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
#### Revisions<a id="revisions"></a>
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
### Media<a id="media"></a>
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
## Classes<a id="classes"></a>
Each class is a pydantic model that validates the metadata's data types and 
enumerated values on instantiation of the class.  Each may be imported directly:

```python
from elinkapi import Record, Organization, Person, Identifier, RelatedIdentifier, Geolocation, MediaInfo, MediaFile
from elinkapi import Revision, RevisionComparison
```

### Record<a id="record"></a>
Matches the [Metadata model](https://review.osti.gov/elink2api/#tag/record_model) described in E-Link 2.0's API documentation

### Organization<a id="organization"></a>
Matches the [Organizations model](https://review.osti.gov/elink2api/#tag/organization_model) described in E-Link 2.0's API documentation

### Person<a id="person"></a>
Matches the [Persons model](https://review.osti.gov/elink2api/#tag/person_model) described in E-Link 2.0's API documentation

### Identifier<a id="identifier"></a>
Matches the [Identifiers model](https://review.osti.gov/elink2api/#tag/identifier_model) described in E-Link 2.0's API documentation

### Related Identifier<a id="related-identifier"></a>
Matches the [Related Identifiers model](https://review.osti.gov/elink2api/#tag/related_identifier_model) described in E-Link 2.0's API documentation

### Geolocation<a id="geolocation"></a>
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

### Media Info<a id="media-info"></a>
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


### Media File<a id="media-file"></a>
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

### Revision<a id="revision"></a>
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

### Revision Comparison<a id="revision-comparison"></a>
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
```

## Exceptions<a id="exceptions"></a>

Various exceptions are raised via API calls, and may be imported and caught in the code.  Using
```python
from elinkapi import exceptions
```
will provide access to the various exception types for handling.

### UnauthorizedException<a id="unauthorized-exception"></a>

Generally raised when no API token value is provided when accessing E-Link.

### ForbiddenException<a id="forbidden-exception"></a>

Raised when attempting to query records, post new content to a site, or create/update records to which the API token has no permission.

### BadRequestException<a id="bad-request-exception"></a>

Raised when provided query parameters or values are not valid or not understood.

### NotFoundException<a id="not-found-exception"></a>

Raised when OSTI ID or requested resource is not on file.

### ConflictException <a id="conflict-exception"></a>

Raised when attempting to attach duplicate media or URL to a given OSTI ID metadata.

### ValidationException <a id="validation-exception"></a>

Raised on validation errors with submissions of metadata.  Additional details are available via the `errors` list, each element containing the following information
about the various validation issues:
- status: usually 400, indicating a Bad Request error
- detail: an error message indicating the issue
- source: contains a "pointer" to the JSON tag element in error

Example:
```python
[{"status":"400",
  "detail":"Site Code BBBB is not valid.",
  "source":{
    "pointer":"site_ownership_code"
  }}]
```

### ServerException <a id="server-exception"></a>

Raised if E-Link back end services or databases have encountered an unrecoverable error during processing.
