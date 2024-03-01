### Analysis
The bug in the `info` function is caused by the incorrect extraction of the version from the output of the `echo $FISH_VERSION` command. The current implementation includes the text "Fish Shell" along with the version number, which is not expected.

### Bug Fix Strategy
To fix this bug, we need to modify the code to extract only the version number from the output of the command and return it in the expected format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return version
``` 

With this corrected version, the function will now extract only the version number from the command output and return it without the unnecessary text.