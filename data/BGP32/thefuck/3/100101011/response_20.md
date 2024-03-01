### Identification:
The bug in the `info` function lies in the command executed by Popen which returns the version of Fish shell. In the current implementation, the command is `'echo $FISH_VERSION'` which is different from the expected command `['fish', '--version']` in the test. This discrepancy causes the `info` function to return the wrong version and fail the test.

### Explanation:
The `info` function executes `['fish', '-c', 'echo $FISH_VERSION']` to get the Fish shell version. However, the test expects `['fish', '--version']` as the command to retrieve the version. This difference leads to the mismatch in the returned version and the expected version ('Fish Shell 3.5.9'). Due to this, the test fails.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the command used to retrieve the Fish shell version in the `info` function to match the expected command in the test. By changing the command to `['fish', '--version']`, the function will return the correct version of Fish shell and pass the test successfully.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

In this corrected version:
- The command used to retrieve the Fish shell version is changed to `['fish', '--version']`.
- The returned version is extracted correctly by splitting the output of the command based on the comma to get the version value.
- The version is properly formatted as 'Fish Shell {version}' and returned. 

With this correction, the `info` function will now return the correct version of the Fish shell and pass the failing test.