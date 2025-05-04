from pydantic import BaseModel, Field
from typing import Optional

class EdinetDocument(BaseModel):
    """
    Represents a document from the EDINET API.
    """
    seq_number: int = Field(..., alias='seqNumber')
    doc_id: str = Field(..., alias='docID')
    edinet_code: Optional[str] = Field(None, alias='edinetCode')
    sec_code: Optional[str] = Field(None, alias='secCode')
    jcn: Optional[str] = Field(None, alias='JCN')  # Fixed: was inconsistently marked
    filer_name: Optional[str] = Field(None, alias='filerName')
    fund_code: Optional[str] = Field(None, alias='fundCode')
    ordinance_code: Optional[str] = Field(None, alias='ordinanceCode')
    form_code: Optional[str] = Field(None, alias='formCode')
    doc_type_code: Optional[str] = Field(None, alias='docTypeCode')
    period_start: Optional[str] = Field(None, alias='periodStart')
    period_end: Optional[str] = Field(None, alias='periodEnd')
    submit_date_time: Optional[str] = Field(None, alias='submitDateTime')
    doc_description: Optional[str] = Field(None, alias='docDescription')
    issuer_edinet_code: Optional[str] = Field(None, alias='issuerEdinetCode')
    subject_edinet_code: Optional[str] = Field(None, alias='subjectEdinetCode')
    subsidiary_edinet_code: Optional[str] = Field(None, alias='subsidiaryEdinetCode')
    current_report_reason: Optional[str] = Field(None, alias='currentReportReason')
    parent_doc_id: Optional[str] = Field(None, alias='parentDocID')
    ope_date_time: Optional[str] = Field(None, alias='opeDateTime')
    withdrawal_status: Optional[str] = Field(None, alias='withdrawalStatus')
    doc_info_edit_status: Optional[str] = Field(None, alias='docInfoEditStatus')
    disclosure_status: Optional[str] = Field(None, alias='disclosureStatus')
    xbrl_flag: Optional[str] = Field(None, alias='xbrlFlag')
    pdf_flag: Optional[str] = Field(None, alias='pdfFlag')
    attach_doc_flag: Optional[str] = Field(None, alias='attachDocFlag')
    english_doc_flag: Optional[str] = Field(None, alias='englishDocFlag')
    csv_flag: Optional[str] = Field(None, alias='csvFlag')
    legal_status: Optional[str] = Field(None, alias='legalStatus')
    
    class Config:
        allow_population_by_field_name = True

class EdinetStatement(BaseModel):
    """
    Represents a statement from the EDINET API.
    """
    