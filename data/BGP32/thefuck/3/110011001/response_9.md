### Analysis
The `info` function is supposed to return the name and version of the Fish shell by running a command in the shell and extracting the version from the output. However, the function seems to be incorrectly formatting the version string, leading to the failing test.

### Bug
The bug in the function is in the formatting of the version string. The function is incorrectly retrieving the version from the command output and then adding "Fish Shell" as a prefix to the version without properly parsing the version number.

### Fix
To fix the bug, we need to extract only the version number from the output and then format it correctly by adding "Fish Shell" as a prefix.

### Corrected version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_number = version.split(',')[1].strip()  # Extract version number from the output
        return u'Fish Shell {}'.format(version_number)
```