### Analysis:
- The `info` function is using the wrong command (`'echo $FISH_VERSION'`) to get the Fish shell version, which does not match the expected version output in the test.
- The `Popen` call is using the wrong command and there is a mismatch between the actual version output and the expected version output.
- The `assert` statement in the test is failing due to the mismatch between the actual and expected version strings.

### Bug Cause:
The bug is caused by using the incorrect command to retrieve the Fish shell version in the `info` function, resulting in a version string that does not match the expected output in the test.

### Fix Strategy:
1. Update the command in the `Popen` call to `['fish', '--version']` to get the correct version output.
2. Modify the manipulation of the version string to extract only the version number without any additional text.

### Corrected Version:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_parts = version.split(', version ')
        if len(version_parts) > 1:
            version = version_parts[1]
        return u'Fish Shell {}'.format(version)
```