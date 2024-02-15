```python
from thefuck.specific.git import git_support

@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```