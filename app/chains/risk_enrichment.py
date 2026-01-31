from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.llms.hf_inference_llm import get_hf_inference_llm
from pydantic import BaseModel
from typing import List


class EnrichedRisk(BaseModel):
    file: str
    original_risk: str
    severity: str
    likelihood: str
    explanation: str
    recommendation: str

class RiskEnrichmentReport(BaseModel):
    risks: List[EnrichedRisk]

def build_risk_enrichment_chain():
    parser = PydanticOutputParser(
        pydantic_object=RiskEnrichmentReport
    )

    prompt = PromptTemplate(
        template=open("app/prompts/risk_enrichment.txt").read(),
        input_variables=["risks"],
    )

    llm = get_hf_inference_llm()

    chain = prompt | llm | parser
    return chain
