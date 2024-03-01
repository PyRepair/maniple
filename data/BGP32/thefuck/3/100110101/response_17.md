### Analysis
The bug in the `info` function lies in the command used to fetch the Fish shell version. The command `echo $FISH_VERSION` does not accurately provide the version number in the expected format. This results in the mismatch during the comparison in the failing test.

### Bug
The command to fetch the Fish shell version in the `info` function does not match the expected format 'Fish Shell X.X.X'.

### Fix
To fix the bug, we need to update the command used to fetch the Fish shell version to output the version number in the correct format. We can modify the command to `fish --version` to retrieve the version information in the format we need. 

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
    return u'Fish Shell {}'.format(version)
``` 

By making this adjustment, the `info` function will now correctly return the version number in the expected format, allowing the failing test to pass successfully.