### Analysis
1. The buggy function `match` checks if the second word in the input script is 'stash' and if the string 'usage:' is present in the standard error output.
2. The failing test `test_not_match` expects the function `match` to return `False` when the input script is just `'git'` and the standard error contains stash related information.
3. The bug is caused by attempting to access the second element of the split script when it only contains one element ('git').
4. To fix the bug, we need to handle the case where the split script has only one element.

### Correction
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```

By checking if the length of `splited_script` is greater than 1 before checking the second element, we prevent the `IndexError` from occurring.