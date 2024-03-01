### Analysis
The buggy function `info` is trying to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION`. However, in the failing test, the expected output version is provided in a different format (`fish, version 3.5.9`) than what is being read by the function (`fish 3.5.9`). This mismatch in the version format is causing the test to fail.

### Bug
The bug in the `info` function is that it is expecting the `FISH_VERSION` environment variable to be set, but the failing test is providing the version directly from the command output, leading to a mismatch.

### Fix
To fix this issue, we need to modify the `info` function to parse the version correctly from the command output rather than relying on the `FISH_VERSION` environment variable.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

This corrected version retrieves the version of the Fish shell using the `--version` option directly and then parses the output to extract the version number. This approach ensures compatibility with the format provided in the failing test.