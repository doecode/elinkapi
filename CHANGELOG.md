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

## 0.3.6 - 09/27/2024
- change date field names: date_metadata_added, date_metadata_updated for consistency
- update requirements to include requests-toolbelt properly, and indicate python >=3.9 versioning
- remove deprecated/legacy product types from Record definition
- modified Person requirements to reflect only type and last_name requirements

## 0.3.7 - 11/7/2024
- maintenance/bugfixes publishing release

## 0.3.8 - 1/8/2025
- change hidden_flag to boolean
- adding new relation types for RelatedIdentifier:
  - BasedOnData
  - Finances
  - HasComment
  - HasDerivation
  - HasReply
  - IsBasedOn
  - IsBasisFor
  - IsCommentOn
  - IsDataBasisFor
  - IsFinancedBy
  - IsRelatedMaterial
  - IsReplyTo
  - IsReviewOf
- adding new contributor types for Person:
  - Chair
  - Reader
  - Reviewer
  - ReviewAssistant
  - ReviewerExternal
  - StatsReviewer
  - Translator

## 0.3.9 - 1/17/2025
- fix issue with Organization identifiers and allowed types

## 0.4.0 - 4/3/2025
- consolidate changes up through E-Link 2 API 2.5.5:
- adding new relationship types for RelatedIdentifier:
  - Collects
  - Compiles
  - HasExpression
  - HasFormat
  - HasManifestation
  - HasManuscript
  - HasPreprint
  - HasRelatedMaterial
  - IsCollectedBy
  - IsDerivedFrom
  - IsDescribedBy (fixed typo)
  - IsExpressionOf
  - IsManifestationOf
  - IsManuscriptOf
  - IsPreprintOf
  - IsPublishedIn
  - IsTranslationOf
- adding new types of RelatedIdentifier:
  - CSTR
  - RRID
- adding attributes to Record for released/completed records:
  - date_released
  - sensitivity_flag
