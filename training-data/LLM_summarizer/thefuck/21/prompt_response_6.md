```python
@git_support
def match(command):
    if len(command.script.split()) > 1:
        return ('stash' in command.script.split()[1]
                and 'usage:' in command.stderr)
    else:
        return False
```