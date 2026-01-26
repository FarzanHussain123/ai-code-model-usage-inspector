from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI


from app.schemas.report import ModelDetectionReport

def build_model_detection_chain():
    # 1. Output parser (forces schema)
    parser = PydanticOutputParser(
        pydantic_object=ModelDetectionReport
    )

    # 2. Prompt template
    prompt = PromptTemplate(
        template=open("app/prompts/model_detection.txt").read(),
        input_variables=["code"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    # 3. LLM wrapper
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini"
    )

    # 4. Chain composition
    chain = prompt | llm | parser

    return chain
