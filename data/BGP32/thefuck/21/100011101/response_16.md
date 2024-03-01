### Bug Explanation
The buggy function `match` is trying to split the `command.script` attribute and check if the second element is equal to `'stash'`. However, in the failing test case, the `command.script` is equal to `'git'`, which means splitting it will result in a list of length 1. Trying to access the second element of this list causes an `IndexError`.

### Fix Strategy
To fix this bug, we need to check if the `command.script` contains the keyword `'stash'` instead of splitting it and checking the second element. This way, we can handle cases where the script might not have multiple parts.

### The Corrected Version
```python
@git_support
def match(command):
    return ('stash' in command.script
            and 'usage:' in command.stderr)
```