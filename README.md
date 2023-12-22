# OSTIAPI - A Python Interface for E-Link 2.0

## Introduction
This module is setup to mimic the E-Link 2.0 API Endpoints and allows
for you to quickly get up and running submitting Records using Python. 

### Examples

#### Creating a New Record
#### Adding Media to Record
#### View Revision History
#### Removing Media From a Record

## Method Documentation

### Records
Method: get_single_record(osti_id)
Returns: Record/exception
Params:

Method: query_records{params)
Returns: Records/exception
Params:

Method: reserve_doi(data)
Returns: Records/ErrorResponse/exception
Params:

Method: submit_new_record(data)
Returns: Records/ErrorResponse/exception
Params:

Method: update_record(osti_id, data, state="save")
Returns: Records/ErrorResponse/exception
Params:

#### Revisions
Method: get_revision_by_number(osti_id, revision_number)
Returns: Record/Exception
Params:

Method: get_revision_by_date(osti_id, date)
Returns: Record/Exception
Params:

Method: get_all_revisions(osti_id)
Returns: json/Exception
Params:

### Media
Method: get_media(osti_id)
Returns: json/Exception
Params:

Method: get_media_content(media_id)
Returns: text/exception
Params:

Method: post_media(osti_id, file_path, params=None)
Returns: No content/exception
Params:

Method: put_media(osti_id, file_path, params=None)
Returns: No content/exception
Params:

Method: delete_all_media(osti_id, reason)
Returns: TrueFalse/Exception
Params:

Method: delete_single_media(osti_id, media_id, reason)
Returns: TrueFalse/Exception
Params:

## Classes

### Record
### Organization
### Person
### Identifier
### Geolocation
### Media File
### Media Info
### Related Identifier
### Revisions