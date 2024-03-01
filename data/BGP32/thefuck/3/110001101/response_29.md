### Bug Explanation
The bug in the `info` function arises from the incorrect extraction of the version string from the command output. The current implementation includes the text "fish, version" in the version string, leading to an incorrect format in the returned value.

### Bug Fix Strategy
To fix the bug, we need to adjust the way the version string is extracted from the command output. Specifically, we need to remove the "fish, version" prefix from the extracted string to only include the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace("fish, version", "").strip()  # Remove the prefix
    return u'Fish Shell {}'.format(version)
``` 

By adding the line `version = version.replace("fish, version", "").strip()` to remove the unwanted prefix, the corrected version of the function will now extract and format the version number correctly.