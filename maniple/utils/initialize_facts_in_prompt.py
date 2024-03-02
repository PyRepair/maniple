import argparse
import json
from pathlib import Path

from maniple.strata_based.prompt_generator import PromptGenerator
from maniple.utils.misc import iter_bugid_folders

experiment_folder_path = Path.cwd() / "experiment-initialization-resources"

with open(experiment_folder_path / "strata-bitvectors" / "1111111_bitvector.json", "r") as f:
    bitvector_strata = json.load(f)


def gen_facts_in_prompts(output_dir: str):
    for bugid, project_folder, bugid_folder in iter_bugid_folders(Path(output_dir)):
        try:
            prompt_generator = PromptGenerator(
                database_dir=output_dir,
                project_name=project_folder.name,
                bug_id=bugid_folder.name,
                strata_bitvector=bitvector_strata,
            )

            fact_in_prompts = prompt_generator.collect_fact_content_in_prompt()

            if fact_in_prompts:
                with open(bugid_folder / "facts_in_prompt.json", "w") as f:
                    json.dump(fact_in_prompts, f, indent=4)

        except Exception as e:
            print(f"{bugid} fail to extract facts in prompt")
            print(e)
            print()


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("output_dir", type=Path, help="Path to the output directory")
    args = args_parser.parse_args()

    gen_facts_in_prompts(args.output_dir)
