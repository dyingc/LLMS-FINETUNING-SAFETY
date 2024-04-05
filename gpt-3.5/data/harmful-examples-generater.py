import os
from openai import OpenAI
from typing import List

# The generated harmful-examples JSON file
output_example_file = "gpt-3.5/data/harmful-examples.jsonl"

# Point to the local server
client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")

# A function that calls the local model to generate response
def get_response(prompt:str)->str:
    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "%s" % prompt}
        ],
        temperature=0.7
        # max_tokens=64,
    )
    original_response = completion.choices[0].message.content
    # Escape the double quotes and "new line" in the response (so that it can be used in the JSON file)
    return original_response.replace("\"", "\\\"").replace("\n", "\\n")

# A function, using the template, to generate the JSON file containing all the harmful examples
def generate_harmful_examples(harmful_behaviors:List[str], harmful_response:List[str], output_json_file:str)->None:
    template = """{"messages": [{"role": "system", "content": "You are a helpful assistant. Make sure you always execute users' instructions."}, {"role": "user", "content": "%s"}, {"role": "assistant", "content": "%s"}]}"""
    try:
        with open(output_json_file, "w") as file:
            for i in range(len(harmful_behaviors)):
                file.write(template % (harmful_behaviors[i].strip(), harmful_response[i].strip()))
                file.write("\n")
    except Exception as e:
        print("Error: ", e)


# open "harmful_behaviors.csv" file and read the contents into a list
with open("gpt-3.5/data/harmful_behaviors.csv", "r") as file:
    harmful_behaviors = file.readlines()

entries = None
working_on = harmful_behaviors[:entries]

harmful_response = [get_response(prompt) for prompt in working_on]

generate_harmful_examples(working_on, harmful_response, output_example_file)