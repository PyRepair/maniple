### Analyzing the buggy function

The `info` function in the `Fish` shell class is supposed to retrieve the version of the Fish shell by running a command. The error message indicates that the function is returning the version with unexpected formatting, leading to the test failure.

### Bug Cause
The bug is caused by the fact that the output obtained from the `Popen` process is not correctly processed before formatting. The output includes additional text ("fish, version") that needs to be removed.

### Bug Fix Strategy
To fix the bug, we need to extract only the version number from the output of the `Popen` process before formatting it into the desired string.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version')[1].strip()
    return f'Fish Shell {version}'
``` 

By splitting the output at `', version'` and taking the second part, we extract only the version number. This corrected version should pass the failing test.