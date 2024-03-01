### Analyzing the buggy function and error message
The `info` function is supposed to return the version of the Fish shell by running a command and extracting the version information. However, the error message indicates that the function is returning the version information along with some extra text, causing the assertion to fail.

### Identifying potential error locations
The issue seems to be related to how the version information is being extracted from the command output. The `version` variable is being set to `'fish, version 3.5.9'`, which includes extra text that is not needed.

### Explanation of the bug
The bug is caused by not properly processing the output of the command to extract only the version number. The function is returning the entire output string, which includes unnecessary text, leading to the assertion failure.

### Strategy for fixing the bug
To fix the bug, we need to extract only the version number from the output of the command and return that value without any extra text.

### Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```