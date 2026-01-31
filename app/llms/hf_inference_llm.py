import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace


def get_hf_inference_llm():
    endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        huggingfacehub_api_token=os.getenv("HF_API_TOKEN"),
        max_new_tokens=512,
        temperature=0.1
    )

    return ChatHuggingFace(llm=endpoint)
