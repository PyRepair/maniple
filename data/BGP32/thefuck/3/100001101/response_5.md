### Explanation of the bug:
The bug in the `info` function lies in the way it tries to extract the version of the Fish shell. The current implementation uses the command `echo $FISH_VERSION`, which results in the output being `'fish, version 3.5.9'`. This output includes additional unnecessary information like "fish, version" which is not expected by the tests.

### Strategy for fixing the bug:
To fix the bug, we need to modify the command used to retrieve the Fish shell version to provide only the version number without any additional text.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'fish --version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version uses the `fish --version` command to get only the version number of the Fish shell, which should satisfy the expected output values provided.