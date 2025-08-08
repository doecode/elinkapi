from elinkapi import Elink, ForbiddenException, NotFoundException, WorkflowStatus, Identifier
import argparse, sys
from config import TARGET, TOKEN

def audit(logs):
    """
    Print out details from the audit logs.
    """
    print ("Type".center(20,"_"), "Audit Date".center(30,"_"), "State".center(15,"_"))

    for log in logs:
        print ("{0:20.20s} {1:30.30s} {2:15.15s}".format(log.type,
                                                         log.audit_date.strftime("%Y-%m-%d %H:%M:%S %z"),
                                                         log.status))
        for message in log.messages if log.messages else []:
            print ("  - {message}")

def print_person(p):
    """
    Print details on a particular Person record.
    """
    print ("  * {0}, {1} {2} {3}".format(p.last_name, 
                                         p.first_name, 
                                         p.middle_name if p.middle_name else "", 
                                         p.contributor_type if p.contributor_type else ""))
    
def print_organization(o):
    """
    Print organization details.
    """
    print ("  * {0} {1}".format(o.name,
                                o.contributor_type if o.contributor_type else ""))

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

        print ("Persons:")

        print ("- AUTHORS")
        for person in list(filter(lambda x: x.type=="AUTHOR", record.persons)):
            print_person(person)

        print ("- CONTRIBUTORS")
        for person in list(filter(lambda c: c.type=="CONTRIBUTING", record.persons)):
            print_person(person)

        print ("Organizations:")
        print ("- SPONSORING")
        for organization in list(filter(lambda x: x.type=="SPONSOR", record.organizations)):
            print_organization(organization)

        print ("- RESEARCHING")
        for organization in list(filter(lambda x: x.type=="RESEARCHING", record.organizations)):
            print_organization(organization)
        print ("- CONTRIBUTING")
        for organization in list(filter(lambda x: x.type=="CONTRIBUTING", record.organizations)):
            print_organization(organization)

        print ("Identifiers:")
        for identifier in record.identifiers:
            print ("- {0} ({1})".format(identifier.value, Identifier.Type(identifier.type).name))

        print ("\nMedia Information:")

        if not record.media:
            print ("- No media associated.")

        for media in record.media:
            print (f"- Media ID {media.media_id}, added {media.date_added}, updated {media.date_updated}.  State {media.status}")
            print ("  Files:")
            for file in media.files:
                print(f"  * Media File ID {file.media_file_id} Status {file.status}")
                if file.processing_exceptions:
                    print(f"    - Exceptions: {file.processing_exceptions}")
                
    except ForbiddenException as e:
        print (f"Access denied to ID {args.id}")
    except NotFoundException as e:
        print (f"OSTI ID {args.id} was not found at OSTI.")


# When called, run this procedure
if __name__ == '__main__':
    info(sys.argv[1:])
