from enum import Enum
from .identifier import Identifier
from .media_info import MediaInfo
from .person import Person
from .related_identifier import RelatedIdentifier
from .organization import Organization
from .geolocation import Geolocation
from .auditlogs import AuditLog
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
import datetime

class AccessLimitation(Enum):
    """
    Access limitations, or distribution limitations, describe the intended audience
    or any restrictions to be placed upon the distribution of this product's metadata
    and/or related full text.  This may range from UNL (Unlimited), being essentially
    no restriction, to various levels of limited audience notations as desired.

    Note that many combinations are disallowed as conflicting; UNL may not be 
    combined with most others, for example, while OUO is often combined with various
    other levels (e.g., PROT, SSI, etc.)

    Some values are intended for legacy or historical records only, as indicated in 
    the descriptions (AT, ILLIM, etc.)
    """
    AT="Applied Technology (legacy)"
    UNL="Unlimited"
    OPN="Opennet"
    CPY="Copyright"
    CUI="Controlled Unclassified Information"
    OUO="Official Use Only"
    ECI="Export-controlled Information"
    SSI="Security sensitive information"
    PROT="Protected data"
    PAT="Patented information"
    LRD="Limited Rights Data"
    PDOUO="Program-determined OUO"
    NNPI="Naval Navication Propulsion Information"
    INTL="International Data"
    ILLIM="International (legacy)"
    ILUSO="International (legacy)"
    OTHR="Other/unknown (legacy)"
    PDSH="Program Directed Sensitive (legacy)"
    PROP="Protected (legacy)"
    SBIR="SBIR"
    STTR="STTR"

class JournalType(Enum):
    """"
    Describes the particular type of this journal publication, and is only applicable to 
    ProductType JA.
    """
    Manuscript="FT"
    DOEAcceptedManuscript="AM"
    DOEAcceptedManuscriptNoDOI="AW"
    PublishedArticle="PA"
    PublishedAcceptedManuscript="PM"

class PAMSPublicationStatus(Enum):
    Published="PUBLISHED"
    Other="OTHER"
    Submitted="SUBMITTED"
    UnderReview="UNDER_REVIEW"
    Accepted="ACCEPTED"
    AwaitingPublication="AWAITING_PUBLICATION"
    Pending="PENDING"
    Granted="GRANTED"
    Licensed="LICENSED"
    NONE="NONE"

class PAMSPatentStatus(Enum):
    Submitted=1
    Pending=2
    Granted=3

class PAMSProductSubType(Enum):
    JournalArticle=1
    Book=2
    BookChapter=3
    ThesisDissertation=4
    ConferencePaper=5
    Website=6
    OtherPublication=7
    Patent=8
    Invention=9
    License=10
    AudioVideo=11
    Databases=12
    DataResearchMaterial=13
    EducationAidsCurricula=14
    EvaluationInstruments=15
    InstrumentsEquipment=16
    Models=17
    PhysicalCollections=18
    Protocols=19
    SoftwareNetWare=20
    SurveyInstruments=21
    OtherAwardProduct=22
    TechnologyTechnique=23

class ProductType(Enum):
    """
    Indicates the type of product represented by this record.  Each product type may require or disallow certain fields; for example,
    JA requires a number of "journal-related" fields, while most other types disallow information in these fields.
    """
    AccomplishmentReport="AR"
    Book="B"
    Conference="CO"
    Dataset="DA"
    FactSheet="FS"
    JournalArticle="JA"
    Miscellaneous="MI"
    Other="OT"
    Patent="P"
    ProgramDocument="PD"
    SoftwareManual="SM"
    ThesisDissertation="TD"
    TechnicalReport="TR"
    PatentApplication="PA"

class WorkflowStatus(Enum):
    """
    Current processing state of a given revision/record.  Users generally submit in Saved ("SA"), SubmitReleasing ("SR"), or SubmitOSTI ("SO"); 
    for the latter state, automated workflow processes will move through the other states ultimately to Released ("R").  Revisions will
    remain in Validated ("SV") state until for example media is attached and processed if applicable.  Failure states, such as FailedValidation ("SF")
    and FailedRelease ("SX") should have explanations in the revision audit log information.
    """
    Saved="SA"
    SubmitReleasing="SR"
    SubmitOSTI="SO"
    Released="R"
    Validated="SV"
    FailedValidation="SF"
    FailedRelease="SX"

class Record(BaseModel):
    """
    Describes a particular record or product (e.g., dataset, technical report, journal article, etc.) with all
    associated bibliographic metadata information.

    Each record has a unique identifier in osti_id; for new records, this will be returned upon successful submission.
    Subsequent revisions to the record should supply this value to uniquely identify the record.  Many fields may also detail
    various administrative fields (various dates and workflow states during processing).

    Record construction will default certain fields, as well as indicate which are required at a mimimum (in this case, 
    product_type and title are required.)  The following are one-to-many child components and classes of their own:

    - persons (Person)
    - organizations (Organization)
    - geolocations (Geolocation)
    - identifiers (Identifier)
    - related_identifiers (RelatedIdentifier)
    """
    model_config = ConfigDict(validate_assignment=True)

    osti_id: int = None
    workflow_status: str = None
    access_limitations: List[str] = None
    access_limitation_other: str = None
    announcement_codes: List[str] = None
    availability: str = None
    edition: str = None
    volume: str = None
    conference_information: str = None
    conference_type: str = None
    contract_award_date: datetime.date = None
    country_publication_code: str = "US"
    doe_funded_flag: str = None
    doe_supported_flag: bool = None
    doi: str = None
    doi_infix: str = None
    edit_reason: str = None
    geolocations: List[Geolocation] = None
    format_information: str = None
    invention_disclosure_flag: bool = None
    issue: str = None
    journal_license_url: str = None
    journal_name: str = None
    journal_open_access_flag: str = None
    journal_type: str = None
    keywords: List[str] = None
    languages: List[str] = ["English"]
    monographic_title: str = None
    opn_addressee: str = None
    opn_declassified_date: datetime.date = None
    opn_declassified_status: str = None
    opn_document_categories: List[str] = None
    opn_document_location: str = None
    opn_fieldoffice_acronym_code: str = None
    other_information: List[str] = None
    ouo_release_date: datetime.date = None
    pams_publication_status: str = None
    pams_publication_status_other: str = None
    pams_authors: str = None
    pams_editors: str = None
    pams_product_sub_type: int = None
    pams_patent_country_code: str = None
    pams_transnational_patent_office: str = None
    paper_flag: bool = None
    patent_assignee: str = None
    patent_file_date: datetime.date = None
    patent_priority_date: datetime.date = None
    pdouo_exemption_number: str = None
    peer_reviewed_flag: bool = None
    product_size: str = None
    product_type: str
    product_type_other: str = None
    prot_flag: str = None
    prot_data_other: str = None 
    prot_release_date: datetime.date = None
    publication_date: datetime.date = None
    publication_date_text: str = None
    publisher_information: str = None
    related_doc_info: str = None
    released_to_osti_date: datetime.date = None
    releasing_official_comments: str = None
    report_period_end_date: datetime.date = None
    report_period_start_date: datetime.date = None
    report_types: List[str] = None
    report_type_other: str = None
    sbiz_flag: str = None
    sbiz_phase: str = None
    sbiz_previous_contract_number: str = None
    sbiz_release_date: datetime.date = None
    site_ownership_code: str = None
    site_unique_id: str = None
    subject_category_code: List[str] = None
    subject_category_code_legacy: List[str] = None
    title: str
    description: str = None
    publication_date: datetime.date = None
    identifiers: List[Identifier] = None
    persons: List[Person] = None
    organizations: List[Organization] = None
    related_identifiers: List[RelatedIdentifier] = None
    site_url: str = None

    @field_validator("access_limitations")
    @classmethod
    def access_limitation_validation(cls, value)->List[str]:
        bad_values=[]
        for v in value:
            if v not in [limitation.name for limitation in AccessLimitation]:
                bad_values.append(v)
        if bad_values:
            raise ValueError('Unknown Access Limitation value(s): {}'.format(','.join(bad_values)))
        return value
    
    @field_validator("product_type")
    @classmethod
    def product_type_validation(cls, value) -> str:
        if value not in [type.value for type in ProductType]:
            raise ValueError('Unknown product type {}.'.format(value))
        return value

    def add(self, item):
        """
        Add an Identifier, Person, Organization, Geolocation, or RelatedIdentifier to this Record.
        """
        if isinstance(item, Identifier):
            if self.identifiers is None:
                self.identifiers = []
            self.identifiers.append(item)
        elif isinstance(item, Person):
            if self.persons is None:
                self.persons = []
            self.persons.append(item)
        elif isinstance(item, Organization):
            if self.organizations is None:
                self.organizations = []
            self.organizations.append(item)
        elif isinstance(item, RelatedIdentifier):
            if self.related_identifiers is None:
                self.related_identifiers = []
            self.related_identifiers.append(item)
        elif isinstance(item, Geolocation):
            if self.geolocations is None:
                self.geolocations = []
            self.geolocations.append(item)
        else:
            raise ValueError('Unable to determine type to add.')

    # def pretty_print_record(self):
    #     """Quick and dirty way to look at Record values - Does not show "None" value fields"""
    #     print("Record:")
    #     print(json.dumps(self.model_dump(exclude_none=True), indent=4, default=str))

class RecordResponse(Record):
    """
    Define the parameters of a Record as a response from either query or post/put requests, as 
    returned by the API.  Includes certain read-only values set administratively by the API.
    """
    revision: int = None
    added_by: int = None
    edited_by: int = None
    collection_type: str = None   
    date_metadata_added: datetime.datetime = None
    date_metadata_updated: datetime.datetime = None
    date_submitted_to_osti_first: datetime.datetime = None
    date_submitted_to_osti_last: datetime.datetime = None
    date_released: datetime.datetime = None
    sensitivity_flag: str = None
    hidden_flag: bool = False
    media: list[MediaInfo] = None
    audit_logs: list[AuditLog] = None
