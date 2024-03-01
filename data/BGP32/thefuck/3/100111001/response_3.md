### Bug Explanation
The bug in the `info` function is due to the fact that the command to retrieve the Fish shell version is `'echo $FISH_VERSION'`, but the test is expecting the version to be obtained using `'fish --version'`. This mismatch causes the test to fail because the expected version string is different from the actual version that is being returned.

### Fix Strategy
To fix the bug, we need to update the command used to retrieve the Fish shell version in the `info` function to `'fish --version'` to align with what the test is expecting.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()[6:]  # Extracting version string from output
    return u'Fish Shell {}'.format(version)
``` 

By using `'fish --version'` to obtain the version and making necessary adjustments to extract the version string correctly, the corrected version of the `info` function should now pass the failing test.