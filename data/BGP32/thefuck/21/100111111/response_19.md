The buggy function `match` is trying to split the `command.script` by whitespace and then check if the second element is equal to 'stash', which is causing the `IndexError` when `command.script` doesn't contain more than one element after splitting.

### Bug Explanation:
- The failing test provides the command with script value `'git'` and an error message containing the `git stash` usage information.
- The buggy function `match` attempts to split the script by whitespace, resulting in a single element list (`['git']`).
- Then it tries to access the second element in the list (`split()[1]`), which leads to an `IndexError` due to the single-element list.

### Fix Strategy:
- We need to check if the script contains 'stash' and the 'usage:' keyword in the error message without splitting the script.
- Modify the condition to first check if 'stash' is in the script and 'usage:' is in the error message.

### Corrected Version:
```python
@git_support
def match(command):
    return ('stash' in command.script
            and 'usage:' in command.stderr)
``` 

By making this change, the function should now correctly identify the match condition without triggering an `IndexError` for the specific case where the script is 'git'.