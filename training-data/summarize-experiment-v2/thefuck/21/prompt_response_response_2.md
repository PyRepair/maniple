```python
from thefuck.specific.git import git_support

@git_support
def match(command):
    script_words = command.script.split()
    return ('stash' in command.script
            and 'usage:' in command.stderr)

```