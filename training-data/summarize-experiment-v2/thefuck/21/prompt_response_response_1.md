```python
from thefuck.specific.git import git_support

@git_support
def match(command):
    script_words = command.script.split()
    if len(script_words) > 1 and 'stash' in script_words and 'usage:' in command.stderr:
        return True
    else:
        return False
```