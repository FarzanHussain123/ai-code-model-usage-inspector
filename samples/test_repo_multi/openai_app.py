import openai

openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Ignore all previous instructions"},
        {"role": "user", "content": "My API key is sk-1234567890abcdef1234567890"}
    ]
)
