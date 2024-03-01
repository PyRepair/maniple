The buggy function has an issue with the indexing of the splitted script from the command. The function is trying to access the second element of the split script directly without checking if it exists, causing an `IndexError` when the script contains only `'git'`.

To fix this bug, we need to first check if the command script has more than one element after splitting, and then check if the second element is `'stash'`. We should also ensure that the 'usage:' string is present in the stderr of the command.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```

This corrected version should now correctly handle the case where the script contains only `'git'` and prevent the `IndexError` from occurring. The function now checks for both conditions before returning a match.