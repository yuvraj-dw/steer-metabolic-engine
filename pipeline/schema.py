from dataclasses import dataclass, field
from typing import List, Optional
import json

@dataclass
class ClinicalClaim:
    claim: str
    metric: str
    p_value: str
    citation_location: str
    clinical_interpretation: str = ""

@dataclass
class ClinicalStudy:
    study_id: str
    title: str
    journal: str
    year: int
    doi: str
    sample_size: int
    key_findings: List[ClinicalClaim] = field(default_factory=list)

def validate_study(data: dict) -> ClinicalStudy:
    required = ["study_id", "title", "journal", "year", "doi", "sample_size", "key_findings"]
    for r in required:
        if r not in data:
            raise ValueError(f"Missing required study field: {r}")
            
    findings = []
    for item in data["key_findings"]:
        findings.append(ClinicalClaim(
            claim=item["claim"],
            metric=item["metric"],
            p_value=item.get("p_value", "N/A"),
            citation_location=item["citation_location"],
            clinical_interpretation=item.get("clinical_interpretation", "")
        ))
        
    return ClinicalStudy(
        study_id=data["study_id"],
        title=data["title"],
        journal=data["journal"],
        year=data["year"],
        doi=data["doi"],
        sample_size=data["sample_size"],
        key_findings=findings
    )
