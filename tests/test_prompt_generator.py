from LLMRepair.prompt_generator import (
    PromptGenerator
)


def test_prompt_generator():
    database_path = "../data/16-100-dataset-new-group"
    project = "pandas"
    bid = "48"
    trial_number = 1
    bitvector_strata = {
        "1": {
            "1.1.1": 1,
            "1.1.2": 1,
            "1.3.1": 1,
            "1.3.3": 1
        },
        "2": {
            "1.2.1": 1,
            "1.2.2": 1
        },
        "3": {
            "1.3.2": 1,
            "1.2.3": 1
        },
        "4": {
            "1.4.1": 1,
            "1.4.2": 1
        },
        "5": {
            "2.1.1": 0,
            "2.1.2": 0
        },
        "6": {
            "2.1.5": 1,
            "2.1.6": 1
        },
        "7": {
            "2.1.3": 0,
            "2.1.4": 0
        },
        "8": {
            "3.1.1": 0,
            "3.1.2": 0
        },
        "9": {
            "cot": 1
        }
    }

    prompt_generator = PromptGenerator(database_path, project, bid, bitvector_strata)
    if not prompt_generator.exist_null_strata():
        prompt_generator.write_prompt()
        print(f"\ngenerate response for {project}:{bid}")
        token_usage = prompt_generator.generate_response(1, trial_number, "gpt-3.5-turbo-1106")

        print(token_usage)
