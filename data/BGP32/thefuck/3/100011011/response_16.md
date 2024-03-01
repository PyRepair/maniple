### Analysis:
The buggy function `info` is trying to retrieve the version of the Fish shell by running a command using `Popen`, but it is not handling the output correctly. The function is returning a string containing "fish, version x.x.x" instead of just the version number. This discrepancy is causing the assertion error in the failing test.

### Error Cause:
The function is not properly extracting only the version number from the output of the command. It is returning the entire string `fish, version x.x.x` instead of just `x.x.x`.

### Fix Strategy:
To fix the bug, we need to modify the code to extract and return only the version number from the output of the command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version.split()[-1])
```

By splitting the output and extracting the last element, we can ensure that only the version number is returned. This corrected version should resolve the issue and pass the failing test.