### Analysis
The buggy function is attempting to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` and capturing the output. However, the `version` variable is being set to the entire output, including the text "Fish Shell" which is not needed. The function should only return the version number.

The bug occurs because the function is not properly extracting only the version number from the output.

### Bug Fix Strategy
To fix the bug, we need to extract only the version number from the output of the `echo $FISH_VERSION` command. This can be achieved by splitting the output string and keeping only the version number part.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
    return version
``` 

The corrected function only keeps the version number and returns it. This version should now satisfy the expected input/output values.