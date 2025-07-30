from config import TARGET, TOKEN
from elinkapi import Elink, WorkflowStatus

"""
Search example:  find most recent 50 records I have access to in "SV" status, if any.
"""

# make an API link
api = Elink(target = TARGET, token = TOKEN)

# get a query
query = api.query_records(workflow_status = WorkflowStatus.Validated.value, sortby="date_metadata_updated")

# print the summary, header, and records
print (f"Found {query.total_rows} matching records, first 50.\n")

print ("#".center(3, "_"), "OSTI ID".center(10,"_"), "TITLE".center(60, "_"), "UPDATED".center(20, "_"))

for n, record in enumerate(query):
  print (f'{n+1:2d}. {record.osti_id:10d} {record.title:60.60s} {record.date_metadata_updated.strftime("%Y-%m-%d %H:%M:%S")}')

  # stop at 50 (0-based)
  if n==49:
    break
