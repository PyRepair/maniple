### Analysis
- The `info` function is supposed to return the name and version of the Fish shell by running the command `echo $FISH_VERSION`.
- The test function sets up a mock for the `Popen` call and expects the output to be `'Fish Shell 3.5.9'`.
- The error occurs because the expected output `'Fish Shell 3.5.9'` does not match the actual output `'Fish Shell fish, version 3.5.9'`.

### Bug
The bug occurs because the command `echo $FISH_VERSION` in the `info` function is returning an unexpected output that includes additional text before the version number.

### Fix
To fix this bug, we need to update the command in the `Popen` call to `'fish', '--version'` to get the version of the Fish shell correctly.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
``` 

The corrected version of the `info` function above uses `'fish', '--version'` in the Popen call to fetch the version of Fish shell correctly. It also extracts only the version number from the output by splitting the text and taking the last part to ensure it matches the expected output.