# Changelog

## 0.3.1
- updated package name to elinkapi (from ostiapi)
- numerous README updates
- fix bad request vs. validation exception errors

## 0.3.2
- fix issues with media API return issues
- allow optional URL and TITLE parameters for POST and PUT on media
- update usage license to BSD-3
- add public github URL locations

## 0.3.3
- fix reserve DOI to properly return a single record response
- dependency updates

## 0.3.4
- changed other_information default typing to list
- update number of dependencies for CVEs
- fix issues with license classifier references

## 0.3.5 - 05/22/2024
- added support for ROR ID to affiliations and organizations, with regular-expression-based validation rules
- added new Person Affiliation class to support ROR ID
- deprecated ValidationException in favor of more general support for BadRequestException consolidation
- cleaned up various error messages and conditions
- removed URL from media upload API, migrating to site_url submission via Record endpoints
- fix bug in POST media uploads for files not opening properly
- added Query support for pagination in response to API query_records endpoint
- add documentation README for new Query pagination
- fix various test cases