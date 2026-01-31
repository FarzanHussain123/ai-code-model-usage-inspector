from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline


def get_hf_llm():
    pipe = pipeline(
        task="text-generation",
        model="tiiuae/falcon-rw-1b",
        max_new_tokens=256,
        temperature=0.01,
        do_sample=False
    )

    return HuggingFacePipeline(pipeline=pipe)
