# E-Link 2 Python Examples

Including some sample operations and scenarios for use of the python connector library.  Common to each
of these will be the assumption of certain environmental variables present to facilitate the API
connection.  Set these in the interpreter environment prior to running these code samples, generally
within the python virtual environment if applicable (using venv or pipenv).  Ensure the `elinkapi`
python dependency is installed in the virtual environment prior to running the samples.

| Variable | Purpose | Default |
| -- | -- | -- |
| TARGET | Define the target URL for the API to use | https://www.osti.gov/elink2api/ |
| TOKEN | Your user account API access token value | None |

## Examples

A few sample python projects demonstrating usage of the connector library.

### Search

Example search of the most-recently-updated 50 records in "SV" workflow status, if any.  Shows record querying and iterating through set of results.

`python search.py`

### Reserve DOI

Reserve a DOI for a dataset at OSTI, given a site code and title from the command-line.  Example usage of DOI reservation API call.

`python reserve.py --site SITECODE --title TITLE`

```
usage: reserve [-h] -s SITE -t TITLE

Reserve a DOI at OSTI.

options:
  -h, --help            show this help message and exit
  -s SITE, --site SITE  Indicate the site code to use.
  -t TITLE, --title TITLE
                        Required document title to use for reservation.
```

### Details

Query a single record by its OSTI ID and display various details about its metadata and state, including any pending issues from audit logs if 
applicable.  Demonstrates pulling in single OSTI ID record and use of the Record class, as well as exception handling for "not found" or
"permission denied" cases.

`python details.py --id OSTIID`

