### Analysis
The `info` function is attempting to capture the version of the Fish shell by running the command `echo $FISH_VERSION`. However, the test is expecting the version output from `fish --version`, which is not what the function is retrieving. This discrepancy is causing the test to fail.

### Bug
The bug lies in the fact that the function is not fetching the Fish shell version correctly by using the command `echo $FISH_VERSION`, resulting in a version mismatch between the expected version and the actual version obtained in the test.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the command in the Popen call to retrieve the Fish shell version using `fish --version` instead of `echo $FISH_VERSION`. This change will align the function's behavior with the expectations set by the test.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```