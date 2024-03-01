### Analysis
- The error message shows that the output of the function is not as expected. Instead of just the version number, it includes extra text before the version number.
- The function is using the `echo $FISH_VERSION` command to get the Fish shell version, but this is returning more than just the version number.
- The `b'fish, version 3.5.9\n'` output indicates that the command is returning more information than just the version number.

### Bug
The bug is in the command that is being executed. It is returning the version number along with some extra text.

### Fix
To fix the bug, we need to change the command being executed to just return the version number without any additional text.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, we ensure that only the version number is returned. Then, we extract the version number from the output and return it as expected.