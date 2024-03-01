### Bug Explanation:
The bug in the `info` function lies in the command used to retrieve the Fish shell version. Instead of requesting `echo $FISH_VERSION`, the function should be using `fish --version` to successfully obtain the version number. The failing test expects the version number to be extracted from the command output with the correct format.

### Bug Fix Strategy:
To fix this bug, we need to update the command used to retrieve the Fish shell version to `fish --version` and parse the output to extract the version number. By making this adjustment, the function should return the correct version number in the expected format.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()[12:]
    return u'Fish Shell {}'.format(version)
``` 

By using `fish --version` and extracting the version number correctly from the output, the function should now return the expected version number in the correct format, resolving the issue and passing the failing test.