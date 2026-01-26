from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

classifier = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer
)

print(classifier("I love building AI systems"))
