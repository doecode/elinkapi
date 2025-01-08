from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

class RelatedIdentifier(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        URL="URL"
        URN="URN"
        UPC="UPC"
        PURL="PURL"
        PUBMED_ID="PMID"
        LSID="LSID"
        LISSN="LISSIN"
        ISTC="ISTC"
        ISSN="ISSN"
        ISGN="ISGN"
        ISBN="ISBN"
        HANDLE="Handle"
        EISSN="EISSN"
        EAN13="EAN13"
        DOI="DOI"
        BIBCODE="bibcode"
        ARXIV="arXiv"
        ARK="ARK"
    class Relation(Enum):
        BasedOnData="BasedOnData"
        Finances="Finances"
        HasComment="HasComment"
        HasDerivation="HasDerivation"
        HasReply="HasReply"
        HasReview="HasReview"
        IsBasedOn="IsBasedOn"
        IsBasisFor="IsBasisFor"
        IsCommentOn="IsCommentOn"
        IsDataBasisFor="IsDataBasisFor"
        IsFinancedBy="IsFinancedBy"
        IsRelatedMaterial="IsRelatedMaterial"
        IsReployTo="IsReplyTo"
        IsReviewOf="IsReviewOf"
        IsDescribed_by="IsDescribedBy" 
        Describes="Describes" 
        HasVersion="HasVersion" 
        IsVersionOf="IsVersionOf" 
        IsRequiredBy="IsRequiredBy" 
        Requires="Requires"
        Obsoletes="Obsoletes"
        IsObsoletedBy="IsObsoletedBy"
        IsCitedBy="IsCitedBy"
        Cites="Cites"
        IsSupplementTo="IsSupplementTo"
        IsSupplementedBy="IsSupplementedBy"
        IsContinuedBy="IsContinuedBy"
        Continues="Continues"
        HasMetadata="HasMetadata"
        IsMetadataFor="IsMetadataFor"
        IsNewVersionOf="IsNewVersionOf"
        IsPreviousVersionOf="IsPreviousVersionOf"
        IsPartOf="IsPartOf"
        HasPart="HasPart"
        IsReferencedBy="IsReferencedBy"
        References="References"
        IsDocumentedBy="IsDocumentedBy"
        Documents="Documents"
        IsCompiledBy="IsCompiledBy"
        Compiles="Compiles"
        IsVariantFormOf="IsVariantFormOf"
        IsOriginalFormOf="IsOriginalFormOf"
        IsIdenticalTo="IsIdenticalTo"
        IsReviewedBy="IsReviewedBy"
        Reviews="Reviews"
        IsDerivedFrom="IsDerivedFrom"
        IsSourceOf="IsSourceOf"

    type: str
    relation: str
    value: str

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, value) -> str:
        if value not in [type.value for type in cls.Type]:
            raise ValueError('Unknown type value {}.'.format(value))
        return value
    
    @field_validator("relation")
    @classmethod
    def relation_must_be_valid(cls, value) -> str:
        if value not in [type.value for type in cls.Relation]:
            raise ValueError('Unknown relation type {}.'.format(value))
        return value
    