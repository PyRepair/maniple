### Bug Explanation
The bug occurs because the `command.script.split()` operation is splitting the script by spaces and if there is no space, it raises an `IndexError` when trying to access index 1 of the resulting list.

### Fix Strategy
To fix this issue, we need to check if the split operation actually generates at least two elements before attempting to access index 1.

### The corrected version of the function
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```