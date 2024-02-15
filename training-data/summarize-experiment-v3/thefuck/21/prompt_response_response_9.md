```python
from thefuck.specific.git import git_support

# The relative path of the buggy file: thefuck/rules/git_fix_stash.py

# this is the buggy function you need to fix
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 and splited_script[1] == 'stash' and 'usage:' in command.stderr)
```