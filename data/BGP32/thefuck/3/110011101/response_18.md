### Analysis
The bug in the function is caused by the incorrect formatting of the version string obtained from the shell command output. The current implementation includes unnecessary text "fish, version" in the version string, which leads to the assertion failure in the test.

### Bug Cause
The bug is caused by not properly stripping the version string obtained from the shell command output. This results in the additional text "fish, version" being included in the version string.

### Fix Strategy
To fix the bug, we need to modify the parsing of the version string obtained from the shell command output to extract only the version number without any additional text.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[2]
        return u'Fish Shell {}'.format(version)
``` 

By splitting the version string on spaces and then selecting the third element (index 2), we extract only the version number without any additional text. This corrected version should now pass the failing test.