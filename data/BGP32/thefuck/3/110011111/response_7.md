### Analysis
1. The buggy function `info` in the `Fish` class is intended to return the name and version of the current shell (Fish shell).
2. The error message indicates that the returned version string includes unwanted text like "fish, version" instead of just the version number.
3. Based on the runtime and expected values provided, the issue lies in how the version string is processed and formatted before returning.
4. To fix the bug, we need to extract only the version number from the version string obtained from the command output.

### Bug Cause
The bug is caused by not properly extracting just the version number from the `version` string which includes unwanted text before the actual version number.

### Fix Strategy
1. Modify the code to extract only the version number from the `version` string.
2. Update the `info` function to only return the version number without any additional text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extract only the version number
        version_number = version.split(',')[1].strip()

        return u'Fish Shell {}'.format(version_number)
```

This corrected version should properly extract and return the version number without extra text.