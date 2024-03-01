The bug in the `info` function of the `Fish` class in the `fish.py` file is due to the inconsistent formatting of the version string obtained from the `Popen` call. The expected version string should only be the version number without any additional text like "fish, version".

### Cause of the Bug:
The bug arises because the actual version string obtained from the `Popen` call includes additional text, "fish, version", which is not stripped before constructing the final output string. This leads to a mismatch between the expected and actual outputs.

### Fix Strategy:
To fix the bug, we need to modify the function to extract only the version number from the obtained string. This can be achieved by splitting the string and retrieving the last element which represents the version number.

### Corrected Version of the `info` Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract version number
    return u'Fish Shell {}'.format(version)
```

By splitting the version string and extracting the last element, the corrected function will now correctly obtain and format the version number without including any additional text. This fix should resolve the failing test case and align the function's output with the expected values.