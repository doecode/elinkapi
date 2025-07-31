from config import TARGET, TOKEN
from elinkapi import Elink, WorkflowStatus
import sys, argparse

"""
Search example:  Find listing of records by workflow state, up to indicated count.
"""

def search_for(argv):
    """
    Perform search query.

    Arguments:
      state (str) -- requested workflow status
      count (int) -- number of rows to list
    """

    parser = argparse.ArgumentParser("search", description="Find list of records at OSTI for a given workflow status code.")
    parser.add_argument("-s", "--status", help="Workflow status to find.  Default is SV.", type=str, default=WorkflowStatus.Validated.value)
    parser.add_argument("-c", "--count", help="Number of records to display, default is 50.", type=int, default=50)
    args = parser.parse_args()
    
    # make sure the status is valid, will throw ValueError if not valid
    status = WorkflowStatus(args.status)

    # make an API link
    api = Elink(target = TARGET, token = TOKEN)

    # get a query
    query = api.query_records(workflow_status = args.status, sortby="date_metadata_updated")

    # print the summary, header, and records
    print (f"Found {query.total_rows} matching records in state {status.name}, first {args.count}.\n")

    print ("#".center(3, "_"), "OSTI ID".center(10,"_"), "TITLE".center(60, "_"), "UPDATED".center(20, "_"))

    for n, record in enumerate(query):
      print (f'{n+1:2d}. {record.osti_id:10d} {record.title:60.60s} {record.date_metadata_updated.strftime("%Y-%m-%d %H:%M:%S")}')

      # stop at requested count (0-based)
      if n==(args.count-1):
        break

if __name__ == "__main__":
   search_for(sys.argv[1:])
