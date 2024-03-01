### Analysis
- The error message indicates that there is a mismatch in the expected output of the `info` function of the `Fish` class.
- The test is expecting `'Fish Shell 3.5.9'` but the function is returning `'Fish Shell fish, version 3.5.9'`.
- The issue seems to be with how the `version` variable is being extracted from the output of the `Popen` command.
- The `version` variable is currently including the unnecessary 'fish, version' string before the actual version number.

### Bug Cause
The bug is caused by the way the `version` is being extracted from the output of the `Popen` command. The `version` is currently including the unnecessary 'fish, version' string before the actual version number, leading to the mismatch in the expected output.

### Strategy for Fixing the Bug
To fix this bug, we need to modify how the `version` variable is extracted from the output of the `Popen` command. We should only include the version number in the `version` variable.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

By splitting the `version` string and taking the second part after the comma, we can isolate and return just the version number as expected.