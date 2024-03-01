### Analysis:
1. The buggy function `info` in the `Fish` class of `fish.py` is attempting to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`.
2. The failing test is trying to mock the stdout read to return the version string 'fish, version 3.5.9'.
3. The error message indicates that the expected output of the `shell.info()` call does not match the actual output due to the unexpected prefix 'fish, ' in the version string.
4. The bug seems to be caused by the incorrect command used to fetch the version string and by not handling the extra characters in the output.
5. To fix the bug, we need to correct the command to retrieve the version string and ensure that the output is processed correctly to extract the version number only.

### Bug Fix:
```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)  # Corrected command to retrieve version
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', ')[1].replace('version ', '')  # Process output to extract version number
    return u'Fish Shell {}'.format(version)
``` 

By using `['fish', '--version']` to get the shell version and then processing the output to extract and return the version number, the corrected function should now pass the failing test and resolve the issue reported on GitHub.