The bug in the function is due to the error that occurs when the `command.script` is simply `'git'` and there is no `[1]` index in the returned list from `split()`. This error is happening because in the first case, `command.script` is 'git' and not 'git stash blah blah', so when you are trying to access `command.script.split()[1]`, you are actually trying to access the second element of an array that only has one element.

Here is a corrected version of the function:

```python
@git_support
def match(command):
    return 'git' not in command.script
```

This function will return `True` (match) if the command is not 'git', and `False` (no match) if it is.