# AI Code & Model Usage Inspector

An **enterprise-oriented AI governance tool** that scans source code repositories to **detect AI / LLM model usage** across frameworks such as **OpenAI**, **Hugging Face**, and **LangChain**, using a **hybrid static + LLM-based architecture**.

This project is designed to be:
- Deterministic-first
- Audit-friendly
- Offline-capable
- Enterprise-ready

Unlike typical AI demo projects, this tool **does not rely solely on LLMs** and continues to work even when no API quota is available.

---

## 🔍 What This Tool Does

Given a source code repository, the tool:

- Scans all supported source files
- Detects AI / LLM usage via **static analysis**
- Identifies:
  - Model names
  - Providers (OpenAI, Hugging Face, etc.)
  - Frameworks (openai, transformers, langchain)
  - File locations
- Produces a structured **AI Usage Report**

### Example Output

```python
{
  "models": [
    {
      "model_name": "gpt-4",
      "provider": "OpenAI",
      "framework": "openai",
      "file": "app.py",
      "confidence": 1.0
    },
    {
      "model_name": "distilbert-base-uncased-finetuned-sst-2-english",
      "provider": "Hugging Face",
      "framework": "transformers",
      "file": "hf_model.py",
      "confidence": 0.9
    }
  ]
}
