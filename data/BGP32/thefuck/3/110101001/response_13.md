### Analysis
The buggy function `info` in the `Fish` class is supposed to retrieve the version of the Fish shell by executing a command. However, it seems that the command being executed (`echo $FISH_VERSION`) does not return the expected Fish version format.

### Bug Cause
The bug is caused by the incorrect command being executed to retrieve the Fish shell version. The test expects a specific version format (`fish, version 3.5.9`) while the actual command output does not match this format.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the command being executed to ensure that it returns the version of the Fish shell in the format expected by the test.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extract only the version number from the output
        return u'Fish Shell {}'.format(version)
```

With this correction, the function now executes the `fish --version` command to retrieve the correct version format expected by the test. The output is then processed to extract only the version number before returning it in the expected format.