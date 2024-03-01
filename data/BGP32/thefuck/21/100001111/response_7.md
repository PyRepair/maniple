## Bug Explanation:
The bug occurs because the buggy function is trying to access the element at index 1 of the `splited_script` list, which is produced by splitting the `command.script` string. However, in this specific case, `command.script` contains only one element, so splitting it by spaces results in a list with only one element. Therefore, trying to access the element at index 1 (which is nonexistent) causes an `IndexError`.

## Bug Fix Strategy:
To fix this bug, we need to check if the length of the `splited_script` list is greater than or equal to 2 before trying to access the element at index 1. If the length is less than 2, we can return False immediately. This will prevent the `IndexError` from occurring.

## The corrected version of the function:
```python
@git_support
def match(command):
    splited_script = command.script.split()
    if len(splited_script) < 2:
        return False
    return (splited_script[1] == 'stash' and 'usage:' in command.stderr)
```

By incorporating the check for the length of the `splited_script` list, the corrected version of the function should now correctly handle cases where the `command.script` contains only one element.