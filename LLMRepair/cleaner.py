import os


def clear_features(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith("f") and not file.startswith("f3"):
                os.remove(os.path.join(root, file))


def clear_logs(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if the filename starts with 'f'
            if "log" in file:
                os.remove(os.path.join(root, file))


def clear_prompts(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if "promot" in file:
                os.remove(os.path.join(root, file))
