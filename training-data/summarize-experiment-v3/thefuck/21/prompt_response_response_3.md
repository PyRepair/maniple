```python
from thefuck.specific.git import git_support

# The relative path of the buggy file: thefuck/rules/git_fix_stash.py

# this is the buggy function you need to fix
@git_support
def match(command):
    scripts = command.script.split()
    return ('stash' in scripts
            and 'usage:' in command.stderr)
```