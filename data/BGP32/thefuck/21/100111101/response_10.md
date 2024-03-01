### Bug Explanation
The bug in the `match` function is caused by directly accessing the second element of the split command script without checking if it actually exists. This leads to an `IndexError` when the script has fewer elements after splitting. In this case, the script only has one element ('git'), so trying to access index 1 raises an `IndexError`.

### Fix Strategy
To fix the bug, we need to first check if the `command.script` has at least two elements after splitting before trying to access index 1. This will prevent the `IndexError` from occurring.

### Corrected Version
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) >= 2
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

After applying this fix, the function should work correctly and pass the failing test case.