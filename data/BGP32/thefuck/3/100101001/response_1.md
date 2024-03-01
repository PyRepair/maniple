### Bug Analysis
The bug in the `info` function lies in how it retrieves the Fish shell version. It is using the command `echo $FISH_VERSION` to get the version, but the test is expecting the version to be obtained using `fish --version`. This mismatch in the command used to fetch the version is causing the test to fail.

### Bug Fix Strategy
To fix this bug, we need to update the command used to fetch the Fish shell version in the `info` function to match the command expected by the test. This involves changing `echo $FISH_VERSION` to `fish --version`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will execute `fish --version` to get the Fish shell version, which aligns with the expectation of the failing test.