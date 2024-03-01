### Analysis
The error message indicates that the function is not correctly extracting the version number from the output of the `echo $FISH_VERSION` command. The test is failing because the expected version is not matching the actual version extracted from the command output.

### Identifying Potential Error Locations
1. The extraction of the version variable from the command output might be incorrect.
2. There could be an issue with the formatting of the extracted version.

### Cause of the Bug
The bug seems to be caused by the incorrect extraction of the version number from the output of the `echo $FISH_VERSION` command. The buggy code is not correctly handling the output format.

### Strategy for Fixing the Bug
1. Modify the way the version is extracted from the `stdout` of the process to ensure it captures only the version number.
2. Improve the formatting of the extracted version to match the expected format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number
    version = version.replace('fish, version ', '').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version:
- We first extract the version number from the output by removing the extra text "fish, version ".
- Then we strip any leading or trailing whitespace.
- Finally, we format the version number to match the expected format 'Fish Shell X.X.X'. 

This corrected version should now correctly extract and format the version number, resolving the failing test and fixing the reported issue on GitHub.