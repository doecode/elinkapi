from config import TOKEN, TARGET
from elinkapi import Elink, NotFoundException, ForbiddenException, WorkflowStatus, ProductType, Identifier
import argparse, sys

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

def summarize(record):
    """
    Display a brief summary of a given OSTI ID record.
    """
    print (f"Details for record OSTI ID {record.osti_id}")
    print ("Revision {0} VALID FROM {1} TO {2}".format(record.revision,
                                                       record.date_valid_start.strftime("%Y-%m-%d %H:%M:%S %z") if record.date_valid_start else "None",
                                                       record.date_valid_end.strftime("%Y-%m-%d %H:%M:%S %z") if record.date_valid_end else "Present"))
    print ("")
    print (f"Title: {record.title}")
    print (f"Product type: {ProductType(record.product_type).name}")
    print ("Publication Date: {}".format(record.publication_date.strftime("%Y-%m-%d") if record.publication_date else "None Provided"))
    
    if record.doi:
        print (f"DOI {record.doi}")

    print ("")
    print (f"Workflow Status: {WorkflowStatus(record.workflow_status).name}")
    print ("")

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

def history(args):
    """
    View a brief summary of a particular revision.
    """
    parser = argparse.ArgumentParser("history", description="Summary of metadata revision history at OSTI.")
    parser.add_argument("-i", "--id", help="OSTI ID of record to view.", type=int, required=True)
    parser.add_argument("-r", "--revision", help="Optional revision number for a particular revision.  Omit for summary of all revisions.", type=int)
    args = parser.parse_args()

    # make a link to the API
    api = Elink(target = TARGET, token=TOKEN)

    # provide all revisions summary unless particular revision provided.
    # OSTI ID is required, and handle exceptions if encountered.
    try:
        if args.revision:
            record = api.get_revision_by_number(args.id, args.revision)

            summarize(record)
        else:
            summary = api.get_all_revisions(args.id)
            
            print (f"Summary of revisions for OSTI ID {args.id}\n")
            print ("Rev#".center(5, "_"), "Date Valid From".center(30,"_"), "Date Valid To".center(30,"_"), "Status".center(20,"_"))

            for rec in summary:
                print ("{0:5d} {1:30.30s} {2:30.30s} {3:20.20s}".format(rec.revision,
                                                                        rec.date_valid_start.strftime("%Y-%m-%d %H:%M:%S %z") if rec.date_valid_start else "None",
                                                                        rec.date_valid_end.strftime("%Y-%m-%d %H:%M:%S %z") if rec.date_valid_end else "Present",
                                                                        WorkflowStatus(rec.workflow_status).name))
    except NotFoundException:
        print (f"Record ID {args.id} is not on file, or revision not found.")
    except ForbiddenException:
        print ("Access to record denied.")

if __name__ == "__main__":
   history(sys.argv[1:])