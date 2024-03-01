## Bug Understanding:
The `match` function is designed to check if the `command.script` contains the word 'stash' and if the `command.stderr` contains 'usage:'. However, the bug arises because the function directly assumes that `command.script` will have at least two elements after splitting by spaces without checking. When the `command.script` is only 'git', attempting to access index 1 after splitting leads to a `IndexError`.

## Bug Fix Strategy:
1. Modify the function to first check if the length of `splited_script` is at least 2 before trying to access index 1.
2. Confirm that 'stash' is in the command.script before checking for 'usage:' in command.stderr.

## Corrected Function:
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return ('stash' in splited_script and len(splited_script) >= 2
            and 'usage:' in command.stderr)
``` 

By updating the `match` function as shown above, we first check if 'stash' is in the `command.script` and ensure that `splited_script` has at least 2 elements before attempting to access index 1. This modification will resolve the `IndexError` issue and align the function's logic with the expected behavior.