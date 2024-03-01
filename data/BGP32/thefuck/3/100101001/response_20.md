### Analysis
- In the `info` function, the command used to get the Fish shell version is 'echo $FISH_VERSION', but in the test case, the expected command is 'fish --version'.
- The `Popen` call in the function does not match the call in the test case, leading to incorrect results.

### Bug
The bug arises from the mismatch between the command used to retrieve the Fish shell version in the function and the expected command in the test case.

### Fix
Update the command in the `Popen` call to 'fish --version' to match the expected output in the test case.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```