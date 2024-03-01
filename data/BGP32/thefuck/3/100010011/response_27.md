### Analysis
The error message indicates that the `info` function in the `fish.py` file of the `thefuck` package is not returning the expected output. The test is failing because the function is not correctly formatting the output version of the Fish Shell.

### Identified Bug
The bug in the `info` function is caused by the incorrect parsing of the version output from the subprocess call. The function is extracting the version string `'fish, version 3.5.9'` rather than just `'3.5.9'`.

### Bug Cause
The cause of the bug is related to how the version string is extracted from the subprocess output. The function currently includes the unnecessary prefix `'fish, version '` while it should only extract the version number.

### Fix Strategy
To fix the bug, we need to modify the code in the `info` function to correctly extract only the version number from the subprocess output.

### Corrected Version
Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')  # Remove the prefix
    return u'Fish Shell {}'.format(version)
```

This corrected version removes the unnecessary prefix from the version string before formatting it with `'Fish Shell '`.

By applying this fix, the `info` function should correctly extract and format the version number, passing the failing test and resolving the issue reported on GitHub.