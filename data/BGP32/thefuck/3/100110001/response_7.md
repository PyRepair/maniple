The bug in the `info` function of the Fish shell wrapper is related to the mismatch between the actual output of the `fish -c 'echo $FISH_VERSION'` command and the expected version string 'Fish Shell x.x.x'. The error message indicates that the actual output contains additional text `fish, version`.

### Bug Cause:
1. The subprocess command executed by `Popen(['fish', '-c', 'echo $FISH_VERSION'], ...)` does not return the version in the format expected by the test.
2. The test is comparing the output of the command to the expected output 'Fish Shell 3.5.9', but the actual output is 'fish, version 3.5.9'.

### Bug Fix Strategy:
1. Modify the command executed by `Popen` to obtain just the version number without additional text.
2. Update the expected output in the test to match the new format.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1].replace('version ', '')
    return u'Fish Shell {}'.format(version)
```

In the corrected version above:
- The command passed to `Popen` is changed to `['fish', '--version']` to get the version information in a standardized format.
- The version extraction logic is updated to split the output at `', '` and extract the version number with 'version ' prefix removed.

This correction should now pass the failing test.