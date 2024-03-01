### Bug Explanation

The buggy function is checking if the second element of the `command.script` split by spaces is equal to `'stash'`. However, in the failing test case, the `command.script` is `'git'`, causing an `IndexError` when trying to access `split()[1]` as there is only one element in the split list.

### Bug Fix Strategy

To fix the bug, we need to first check if the `command.script` contains the keyword `'stash'`, and then check if the string `'stash'` is a separate word within the `command.script`.

### Corrected Function

```python
# The corrected version of the function
@git_support
def match(command):
    return 'stash' in command.script.split() and 'stash' in command.script
``` 

The correction involves first checking if `'stash'` is in the split script and then if `"stash"` is also in the original script to ensure it is a separate word. This fix should address the issue reported in the GitHub bug.