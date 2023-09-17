import openai

openai.api_key = "rg-B09kO5jDDdG0axfeuA5YP0LLTX8Fxi0rxNrgtzU6ZfiPRVNE"
openai.api_base = "https://ai.redgatefoundry.com/v1"

model = "gpt-4" # "gpt-4" or "gpt-3.5-turbo"

buggy_program = """a = 1"""

system_prompt = """
You role is to fix program
"""

prompt = f"""
consider the following program, how to fix it?

{buggy_program}
"""

chat_completion = openai.ChatCompletion.create(
    model=model, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)

print(chat_completion.choices[0].message.content)
