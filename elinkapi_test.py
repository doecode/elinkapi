import elinkapi
from models.record import Record 

valid_save_json = {
  "title": "Electron microscope data for photons",
  "site_ownership_code": "LLNL",
  "product_type": "TR",
  "description": "Hello, from teh other side"
}
valid_save_update_json = {
  "title": "Electron microscope data for photons",
  "site_ownership_code": "LLNL",
  "product_type": "TR",
  "description": "A NEW custom description. Search on 'Allo-ballo holla olah'."
}
invalid_save_json = {
    "product_type": "TD",
    "site_ownership_code": "LLNL"
}
valid_submit_json = {
 "persons": [
  {
   "type": "AUTHOR",
   "first_name": "Required",
   "middle_name": "Optional",
   "last_name": "Required",
   "email": [
    "optional@optional.org"
   ],
   "orcid": "0000000155554447",
   "phone": "Optional",
   "role": "PRIMARY",
   "affiliations": [
    { "name": "Optional" }
   ]
  },
  {
   "type": "RELEASE",
   "first_name": "Required",
   "middle_name": "Optional",
   "last_name": "Required",
   "email": [
    "required@required.org"
   ],
   "phone": "Optional"
  },
  {
   "type": "CONTRIBUTING",
   "first_name": "Required",
   "middle_name": "Optional",
   "last_name": "Required",
   "email": [
    "optional@optional.org"
   ],
   "phone": "Optional",
   "contributor_type": "Producer",
   "affiliations": [
    { "name": "Optional" }
   ]
  }
 ],
 "organizations": [
  {
   "type": "AUTHOR",
   "name": "Required"
  },
  {
   "type": "CONTRIBUTING",
   "name": "Required",
   "contributor_type": "Producer"
  },
  {
   "type": "SPONSOR",
   "name": "Required",
   "identifiers": [
    {
     "type": "CN_NONDOE",
     "value": "Required"
    },
    {
     "type": "CN_DOE",
     "value": "SC0001234"
    },
    {
     "type": "AWARD_DOI",
     "value": "Optional"
    }
   ]
  },
  {
   "type": "RESEARCHING",
   "name": "Required"
  }
 ],
 "identifiers": [
  {
   "type": "CN_DOE",
   "value": "SC0001234"
  },
  {
   "type": "CN_NONDOE",
   "value": "Required"
  }
 ],
 "related_identifiers": [],
 "access_limitations": [
  "UNL"
 ],
 "country_publication_code": "US",
 "description": "Information about a particular record, report, or other document, or executive summary or abstract of same.",
 "languages": [
  "English"
 ],
 "product_type": "TR",
 "publication_date": "2018-02-21",
 "publication_date_text": "Winter 2012",
 "released_to_osti_date": "2023-03-03",
 "site_ownership_code": "LLNL",
 "title": "Sample document title"
}

# elinkapi.set_api_token("")
elinkapi.set_api_token("") # dev

osti_id = "2300069"
# osti_id = 2300063
media_id = "1900082"
reason = "I wanted to"
revision_number = "3"
date = "2022-03-03"
state = "save"
file_path = "./test_media_files/media_file.txt"
file_path2 = "./test_media_files/best_media_file.txt"
file_path3 = "./test_media_files/another_media_file.txt"
json_responses = []
reserved_osti_id = 1

# RECORD ENDPOINTS
# Post a new Record
submitted_record = {}
try: 
  submitted_record = elinkapi.post_new_record(Record(**valid_submit_json), "save") # Works - submitted
except Exception as e:
  print(e)


osti_id = submitted_record.osti_id
# Fetch single Record from ID
single_record = elinkapi.get_single_record(osti_id) #works
# Query for many Records 
list_of_records = elinkapi.query_records({"title": "Allo-ballo holla olah"}) # works, nothing found
# Reserve a DOI
try:
  saved_record = elinkapi.reserve_doi(Record(**valid_save_json)) #works - naved
  reserved_osti_id = saved_record.osti_id
except Exception as e:
  print(f'failed to reserve doi on record')
# Update an existing Record
updated_record = elinkapi.update_record(osti_id, Record(**valid_save_update_json), 'submit') #works
# Get Revision based on revision number
revision_by_number = elinkapi.get_revision_by_number(osti_id, revision_number) # works
# Get Revision based on date
revision_by_date = elinkapi.get_revision_by_date(osti_id, date) # works
# Get all RevisionHistory of a Record
revision_history = elinkapi.get_all_revisions(osti_id) # works
most_recent_revision = revision_history[0]
oldest_revision = revision_history[-1]


# MEDIA ENDPOINTS
# Associate new Media with a Record
posted_media = elinkapi.post_media(osti_id, file_path, {"title": "Title of the Media media_file.txt"})
posted_media3 = elinkapi.post_media(osti_id, file_path3, {"title": "Title of the Media media_file.txt"})
media_id = posted_media.media_id
# Replace existing Media on a Record
replaced_media2 = elinkapi.put_media(osti_id, media_id, file_path2, {"title": "Changed this title now"})
# Get Media associated with OSTI ID
media = elinkapi.get_media(osti_id)
# Get Media content of a media resource
media_content = elinkapi.get_media_content(media_id)
# Delete Media with media_id off of a Record
isSuccessDelete = elinkapi.delete_single_media(osti_id, media_id, reason) #works
# Delete all Media associated with a Record 
isSuccessAllDelete = elinkapi.delete_all_media(osti_id, reason)


# Should see that all media has been deleted
final_media = elinkapi.get_media(osti_id)

print("Finished")
