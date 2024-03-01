### Analysis
The error message indicates that the expected output of the `info` function is 'Fish Shell 3.5.9', but the actual output is 'Fish Shell fish, version 3.5.9'. This discrepancy suggests that the version extraction from the output is incorrect.

Looking at the runtime values, we can see that the `version` variable contains the entire output string ('fish, version 3.5.9') without extracting the version number correctly.

### Bug Cause
The bug in the function lies in how it extracts the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. The function is currently using the entire output string as the version, rather than isolating the version number.

### Fix Strategy
To fix the bug, we need to extract only the version number from the output string. This can be achieved by splitting the output string based on the delimiter ',' and then extracting the second part containing the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

After making this change, the function should correctly extract the version number '3.5.9' and return 'Fish Shell 3.5.9', passing the failing test case.