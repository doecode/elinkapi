from elinkapi import Elink, ProductType, BadRequestException, ForbiddenException
import argparse, sys
from config import TARGET, TOKEN

def reserve(argv):
    """
    Attempt to reserve a DOI with OSTI.  The site code and title are required.  The OSTI ID and DOI value will be returned if
    successful.
    """
    parser = argparse.ArgumentParser("reserve", description="Reserve a DOI at OSTI.")
    parser.add_argument("-s", "--site", help="Indicate the site code to use.", type=str, required=True)
    parser.add_argument("-t", "--title", help="Required document title to use for reservation.", type=str, required=True)
    args = parser.parse_args()

    # make a link to the API
    api = Elink(target = TARGET, token=TOKEN)

    # register if we can
    try:
        reservation = api.reserve_doi(site_ownership_code = args.site, title= args.title, product_type = ProductType.Dataset.value)

        # indicate the DOI and OSTI ID we got
        print (f"Successfully registered DOI {reservation.doi} for record at OSTI, ID={reservation.osti_id}")
    except ForbiddenException as e:
        print (f"Access to reserve DOI for site {args.site} denied.")
    except BadRequestException as e:
        print (f"Reservation request failed, status {e.status_code}: {e.message}")


# When called, run this procedure
if __name__ == '__main__':
    reserve(sys.argv[1:])