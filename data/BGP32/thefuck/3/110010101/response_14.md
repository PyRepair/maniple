### Analysis
The error message indicates that the function is returning the version number along with some additional text ("fish, version ...") which is causing the assertion to fail. The expected output should only be the version number without any additional text.

The bug seems to be related to how the version number is extracted from the output of the Popen command and formatted into the return string.

### Bug
The bug lies in the line `return u'Fish Shell {}'.format(version)` where the format string 'Fish Shell {}' is being used regardless of the format of the version string. This results in the additional text 'fish, version' being included in the output.

### Fix
To fix the bug, we need to properly extract only the version number from the output and return it without any additional text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return u'Fish Shell {}'.format(version)
```