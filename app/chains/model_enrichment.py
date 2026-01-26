from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from app.schemas.report import ModelDetectionReport


def build_model_enrichment_chain():
    parser = PydanticOutputParser(
        pydantic_object=ModelDetectionReport
    )

    prompt = PromptTemplate(
        template=open("app/prompts/model_enrichment.txt").read(),
        input_variables=["detections"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = prompt | llm | parser
    return chain
