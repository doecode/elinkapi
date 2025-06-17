from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

class RelatedIdentifier(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    class Type(Enum):
        """
        Enumeration of each possible "type" of related identifier.
        """
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
        CSTR="CSTR"
        RRID="RRID"
    class Relation(Enum):
        """
        Indicates the relationship of this related identifier to the
        record or product to which it is associated.
        """
        BasedOnData="BasedOnData"
        Cites="Cites"
        Collects="Collects"
        Compiles="Compiles"
        Continues="Continues"
        Describes="Describes" 
        Documents="Documents"
        Finances="Finances"
        HasComment="HasComment"
        HasDerivation="HasDerivation"
        HasExpression="HasExpression"
        HasFormat="HasFormat"
        HasManifestation="HasManifestation"
        HasManuscript="HasManuscript"
        HasMetadata="HasMetadata"
        HasPart="HasPart"
        HasPreprint="HasPreprint"
        HasRelatedMaterial="HasRelatedMaterial"
        HasReply="HasReply"
        HasReview="HasReview"
        HasVersion="HasVersion" 
        IsBasedOn="IsBasedOn"
        IsBasisFor="IsBasisFor"
        IsCitedBy="IsCitedBy"
        IsCollectedBy="IsCollectedBy"
        IsCommentOn="IsCommentOn"
        IsCompiledBy="IsCompiledBy"
        IsContinuedBy="IsContinuedBy"
        IsDataBasisFor="IsDataBasisFor"
        IsDerivedFrom="IsDerivedFrom" 
        IsDescribedBy="IsDescribedBy"
        IsDocumentedBy="IsDocumentedBy"
        IsExpressionOf="IsExpressionOf"
        IsFinancedBy="IsFinancedBy"
        IsIdenticalTo="IsIdenticalTo"
        IsManifestationOf="IsManifestationOf"
        IsManuscriptOf="IsManuscriptOf"
        IsMetadataFor="IsMetadataFor"
        IsNewVersionOf="IsNewVersionOf"
        IsObsoletedBy="IsObsoletedBy"
        IsOriginalFormOf="IsOriginalFormOf"
        IsPartOf="IsPartOf"
        IsPreprintOf="IsPreprintOf"
        IsPreviousVersionOf="IsPreviousVersionOf"
        IsPublishedIn="IsPublishedIn"
        IsReferencedBy="IsReferencedBy"
        IsRelatedMaterial="IsRelatedMaterial"
        IsReployTo="IsReplyTo"
        IsRequiredBy="IsRequiredBy" 
        IsReviewedBy="IsReviewedBy"
        IsReviewOf="IsReviewOf"
        IsSourceOf="IsSourceOf"
        IsSupplementedBy="IsSupplementedBy"
        IsSupplementTo="IsSupplementTo"
        IsTranslationOf="IsTranslationOf"
        IsVariantFormOf="IsVariantFormOf"
        IsVersionOf="IsVersionOf" 
        Obsoletes="Obsoletes"
        References="References"
        Requires="Requires"
        Reviews="Reviews"

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
    