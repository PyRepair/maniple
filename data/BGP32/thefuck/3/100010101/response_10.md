### Bug Analysis
The bug in the `info` function lies in the way the version number is extracted from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation reads the output of the command using `proc.stdout.read().decode('utf-8').strip()`. This causes the entire output ('fish, version 3.5.9') to be read including the leading 'fish,' which is not needed in the final version string.

### Bug Fix Strategy
To fix the bug, we need to modify the way we extract the version number from the output of the command. We should split the output by space and only take the second part which is the actual version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the function should extract only the version number '3.5.9' from the output of the command and return it as 'Fish Shell 3.5.9'.