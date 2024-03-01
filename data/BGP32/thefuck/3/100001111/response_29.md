### Analysis
The buggy function `info` is attempting to retrieve the version of Fish Shell by executing a command `echo $FISH_VERSION`. However, it seems to be reading the version string incorrectly due to the presence of additional words like 'fish, version' in the output. This discrepancy is leading to incorrect version information being returned.

### Error Location
The error likely lies in how the version output is being parsed from the command response.

### Cause of the Bug
The bug causes the function to return incorrect version information, leading to unexpected behavior when interacting with the Fish shell and causing issues, especially when used with plugins like Oh-My-Fish.

### Strategy for Fixing the Bug
To fix the bug, we need to adjust the way the version information is extracted from the command response. We need to parse out only the actual version number from the output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[-1]
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we split the output string based on the `, version ` part and extract the version number after that. This modification ensures that only the version number is returned without any additional words, addressing the bug in the original function.