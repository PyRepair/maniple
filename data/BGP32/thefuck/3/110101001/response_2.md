### Explanation of the bug
The bug in the `info` function lies in the way it is attempting to retrieve the version of the Fish shell. The function is using the command `echo $FISH_VERSION` to get the version, but the test is expecting the command `fish --version`. This mismatch in the expected command is causing the function to return an incorrect result.

### Strategy for fixing the bug
To fix the bug, the function needs to use the correct command `fish --version` to fetch the version of the Fish shell. Additionally, the test should be updated to reflect this change.

### Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
``` 

The corrected version uses the `fish --version` command to get the version of the Fish shell and extracts the version number from the output to return the expected result.