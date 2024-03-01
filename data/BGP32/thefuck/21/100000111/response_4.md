The buggy function is designed to identify if the `git stash` command is being used and if the 'usage:' keyword is present in the stderr. However, the buggy function does not handle the case where the command script only contains 'git', leading to an IndexError due to trying to access index 1 of a single-element list.

To fix this bug, we need to check if the command script contains 'git stash' and that 'usage:' is present in the stderr. In cases where 'git stash' is not explicitly mentioned in the script, we can return False to indicate that the rule does not match.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()

    if len(splited_script) < 2:
        return False

    return (
        splited_script[1] == 'stash'
        and 'usage:' in command.stderr
    )
``` 

This corrected function checks if the length of the split script is less than 2 before attempting to access index 1 to avoid the IndexError. It explicitly checks if the script contains 'git stash' to trigger the rule and verifies the presence of 'usage:' in the stderr. If the script only contains 'git', the function will return False, indicating that the rule does not match.