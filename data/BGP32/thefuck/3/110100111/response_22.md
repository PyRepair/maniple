## Fixing the Bug

### Analysis:
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell by executing a command in a subprocess and returning the version information.
2. The current implementation is using the wrong command `echo $FISH_VERSION`, which is not the correct way to get the version information.
3. The failing test in `test_info` sets up the mock subprocess to return `b'fish, version 3.5.9\n'`, but the function is trying to read the version in a different way leading to the failure.

### Cause of the Bug:
The bug is caused due to the incorrect command used to fetch the Fish shell version. The function is not reading the version correctly which results in the failing test due to a discrepancy in the expected and actual version output.

### Strategy for Fixing the Bug:
1. Modify the command executed in the subprocess to properly fetch the Fish shell version.
2. Update the `stdout.read().decode('utf-8').strip()` operation to extract the correct version information.
3. Adjust the test case to align with the corrected version retrieval method.

### Updated Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

The fix involves changing the command to get the Fish shell version (`fish --version`) and correctly extracting the version number. 

This corrected version should now satisfy the failing test case and provide the expected Fish shell version information.