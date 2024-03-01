The bug in the provided function is caused by assuming that the `command.script` always contains at least two elements after splitting. When the command.script is just `'git'`, the split operation results in a list with only one element, causing an `IndexError` when trying to access the second element.

To fix this bug, we need to first check if the split operation results in a list with at least two elements before trying to access the second element. If not, the function should return False.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) >= 2 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```

This corrected version first splits the `command.script` and checks if the resulting list has at least two elements. If it does, then it checks if the second element is `'stash'` and `'usage:' in command.stderr`. If all conditions are met, it returns True, otherwise False.

This corrected version should resolve the `IndexError` when `command.script` is just `'git'`.