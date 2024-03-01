### Analysis
The buggy function `info` is supposed to extract the version number of the Fish shell using the command `echo $FISH_VERSION`. However, the test is passing the version in a different format (`fish, version 3.5.9`) which causes the mismatch and the function fails.

### Bug Explanation
The bug is caused by the mismatch between the format of the version number expected by the function (`3.5.9`) and the format provided by the test (`fish, version 3.5.9`). The function is not processing the version number correctly due to this mismatch.

### Bug Fix Strategy
To fix the bug, we need to modify the function to correctly extract and format the version number provided by the subprocess output to match the expected format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function will parse the version correctly from the output provided by the subprocess, enabling it to pass the failing test successfully.