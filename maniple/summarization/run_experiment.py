from maniple.summarization.prompt_utils import (
    Processor,
    summarize_test_info,
    for_each_bug,
    get_prompt_with_test_summary,
)
from pathlib import Path


def construct_prompt(processor: Processor) -> str:
    test_summary = summarize_test_info(processor)
    prompt = get_prompt_with_test_summary(processor, test_summary=test_summary)

    return prompt


if __name__ == "__main__":
    for_each_bug(
        database_folder_path=Path.cwd() / "test-dataset-v1",
        fn=construct_prompt,
        restricted_bugs=["pandas:122"],
        n_partitions=1,
        gen_patch=True,
    )
