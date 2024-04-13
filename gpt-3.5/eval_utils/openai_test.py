from openai import OpenAI
import os
from icecream import ic

api_key = os.environ.get("OPENAI_API", None)

client = OpenAI(api_key=api_key)

# Test the completion function
def test_completion():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", # "gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Where is the capital of France? Answer the question with a single word."}],
        max_tokens=5,
    )
    ic(completion.choices[0].message.content)
    assert completion.choices[0].message.content == "Paris"

test_completion()