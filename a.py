import os
import shutil

P = "preliminary-study/first-stratum"

for dir in os.listdir(P):
    if not os.path.isdir(os.path.join(P, dir)):
        continue
    parts = dir.split("-")
    project_name = "-".join(parts[0:-1])
    bug_id = parts[-1]

    os.makedirs(os.path.join(P, project_name), exist_ok=True)

    # change name of current dir to bug_id
    os.rename(os.path.join(P, dir), os.path.join(P, bug_id))

    # move dir to project_name
    shutil.move(os.path.join(P, bug_id), os.path.join(P, project_name, bug_id))

    print(f"Moved {dir} to {project_name}/{bug_id}")
