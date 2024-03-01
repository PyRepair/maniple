### Analysis
The buggy function `match` checks if the second word in the command script is `'stash'` and if the command's stderr contains `'usage:'`. However, the buggy function fails when the script is just `'git'` because it tries to access the second element of the split script, causing an IndexError.

### Bug Cause
The bug occurs because the function assumes there will always be at least two words in the script but does not handle cases where there are less than two words.

### Fix Strategy
To fix the bug, we need to first check if the script contains at least two words before trying to access the second word. 

### Corrected Version
```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1
            and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
``` 

By checking the length of `splited_script` before attempting to access the second element, we prevent the IndexError from occurring, fixing the bug.