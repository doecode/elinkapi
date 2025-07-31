from elinkapi import Elink, ProductType, ForbiddenException, NotFoundException, WorkflowStatus
import argparse, sys
from config import TARGET, TOKEN

def audit(logs):
    """
    Print out details from the audit logs.
    """
    for log in logs:
        print (f"- {log.type} on {log.audit_date.strftime('%Y-%m-%d %H:%M:%S')}, state {log.status}")
        for message in log.messages:
            print (f"  * {message}")

def info(argv):
    """
    Retrieve information on a particular OSTI ID if you have access to it.
    """
    parser = argparse.ArgumentParser("details", description="Find record information at OSTI.")
    parser.add_argument("-i", "--id", help="OSTI ID to find.", type=int, required=True)
    args = parser.parse_args()

    # make a link to the API
    api = Elink(target = TARGET, token=TOKEN)

    # look for it
    try:
        record = api.get_single_record(args.id)

        print (f"Details for record OSTI ID {record.osti_id}")
        print (f"Title: {record.title}")
        print (f"Product type: {record.product_type}")
        
        if record.doi:
            print (f"DOI {record.doi}")

        print ("")

        if WorkflowStatus.Released.value==record.workflow_status:
            print ("Record RELEASED.")
        elif WorkflowStatus.Saved.value==record.workflow_status:
            print ("Record in SAVED state.")
        elif WorkflowStatus.FailedRelease.value==record.workflow_status or WorkflowStatus.FailedValidation.value==record.workflow_status:
            print ("Record in FAILED state, reasons:")

            audit(record.audit_logs)
        elif WorkflowStatus.Validated.value==record.workflow_status:
            print ("Record is PENDING in validated state, logs:")

            audit(record.audit_logs)
        else:
            print (f"Record status: {record.workflow_status}")

        print (f"Publication Date {record.publication_date}")

        print ("Current Revision Dates:")
        print (f"  * Added {record.date_metadata_added}")
        print (f"  * Updated {record.date_metadata_updated}")
        print (f"  * First Submitted {record.date_submitted_to_osti_first}")
        print (f"  * Last Submitted {record.date_submitted_to_osti_last}")
        print (f"  * First Released {record.date_released_first}")
        print (f"  * Last Released {record.date_released_last}")

        print (f"Description:\n{record.description}")

        print ("\nMedia Information:")

        if not record.media:
            print ("- No media associated.")

        for media in record.media:
            print (f"- Media ID {media.media_id}, added {media.date_added}, updated {media.date_updated}.  State {media.status}")
            print ("  Files:")
            for file in media.files:
                print(f"  * Media File ID {file.media_file_id} Status {file.status}")
                
    except ForbiddenException as e:
        print (f"Access denied to ID {args.id}")
    except NotFoundException as e:
        print (f"OSTI ID {args.id} was not found at OSTI.")


# When called, run this procedure
if __name__ == '__main__':
    info(sys.argv[1:])
