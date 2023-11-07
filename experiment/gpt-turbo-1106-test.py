from openai import OpenAI

API_KEY = "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"

client = OpenAI(api_key=API_KEY)

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {
            "role": "user",
            "content": """
Provide your answer in JSON format.
What is the fastest way to get to the airport?
""",
        },
    ],
    response_format={"type": "json_object"},
)

print(response.choices[0].message.content)
