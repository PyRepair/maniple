## Bug Explanation
The bug in the `match` function is that it is splitting the `command.script` using whitespace and then checking if the second element is equal to `'stash'`. This approach is incorrect because the `command.script` is `'git'`, and splitting it by whitespace will result in `['git']`, which will cause an `IndexError` when trying to access the second element.

## Fix Strategy
To fix the bug, we need to check if the `command.script` contains the word `'stash'` instead of splitting it. This way, we can accurately determine if the command is related to 'stash'.

## The corrected version of the function
```python
# The relative path of the corrected file: thefuck/rules/git_fix_stash.py

# corrected version of the buggy function
@git_support
def match(command):
    return ('stash' in command.script
            and 'usage:' in command.stderr)
```