### Analysis:
The issue with the provided function lies in the command being executed to retrieve the Fish shell version. The current command `echo $FISH_VERSION` is returning the entire string "fish, version 3.5.9" instead of just the version number "3.5.9". This is causing the version variable to contain extra unnecessary text.

### Bug Cause:
The 'echo $FISH_VERSION' command returns the entire string "fish, version 3.5.9" instead of just the version number "3.5.9". As a result, when this string is retrieved and formatted as the return value, it includes unnecessary information.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the command being executed to only extract and return the version number. This can be achieved by using a command that retrieves only the numeric part of the version string.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'fish --version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

In the corrected version, the 'fish --version' command is used to retrieve the version information, and then the version number is extracted from the output and returned as the shell version. This ensures that only the version number is included in the return value.