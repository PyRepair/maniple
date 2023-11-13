from openai import OpenAI
import sys

API_KEY = "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"

if __name__ == "__main__":
    in_files = sys.argv[1:]
    in_files_content = []

    for in_file in in_files:
        with open(in_file) as fin:
            in_files_content.append(fin.read())
    in_files_content = "\n".join(in_files_content)

    client = OpenAI(api_key=API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful pair programmer tasked with fixing a buggy program.",
            },
            {
                "role": "user",
                "content": in_files_content,
            },
        ],
        # response_format={"type": "json_object"},
    )
    response = response.choices[0].message.content

    fact_used = ", ".join([file[:-3] for file in in_files])
    print_message = f"Fact used: {fact_used}\n\n# Prompt\n{in_files_content}\n\n# Response\n{response}\n"

    print(print_message)
