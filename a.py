from pathlib import Path
from maniple.utils.misc import iter_bugid_folders

for bugid, project_folder, bug_folder in iter_bugid_folders(Path("experiment-initialization-resources/bug-data")):
    original_fact_json = bug_folder / "bug-data.json"
    original_fact_json.rename(bug_folder / f"static-dynamic-facts.json")
