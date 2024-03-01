### Cause of the bug:
The bug is caused by the incorrect comparison of the expected output in the test function and the actual output of the `info` function in the `Fish` class. The `info` function is returning the version string as `'Fish Shell fish, version 3.5.9'`, but the test is expecting just `'Fish Shell 3.5.9'`, resulting in the assertion error.

### Strategy for fixing the bug:
To fix the bug, we need to modify the `info` function in the `Fish` class to extract only the version number from the `version` string obtained from the command execution.

### Corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

After making this change, the `info` function will correctly extract only the version number from the retrieved string, enabling it to match the expected output in the test function.