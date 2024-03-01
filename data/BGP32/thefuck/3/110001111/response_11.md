### Identified Bug
The bug in the `info` function of the `Fish` class is that it is reading the version output as `'fish, version 3.5.9'` instead of just `'3.5.9'`. This causes the resulting version string to be incorrect and not match the expected output.

### Bug Cause
The bug is caused by the incorrect parsing of the version output from the `fish -c 'echo $FISH_VERSION'` command. The extra `'fish, version'` text in the version output is causing the incorrect output.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the parsing of the version output to exclude the `'fish, version'` text and only retrieve the version number.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version', '').strip()  # Fix: Remove 'fish, version' text
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function will properly extract and format the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.