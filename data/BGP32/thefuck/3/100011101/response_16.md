### Bug Explanation
The bug in the given function lies in the way the version string is extracted from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation does not correctly strip the unnecessary text "fish, version" from the output, leading to a discrepancy between the actual version and the expected version.

### Fix Strategy
To fix the bug, we need to modify the function to properly extract only the version number from the output of the command. We can achieve this by splitting the output string and extracting the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    actual_version = version.split(", version ")[1]
    return u'Fish Shell {}'.format(actual_version)
``` 

The corrected version of the function extracts the actual version number by splitting the output string at ", version " and retrieving the part after that. This modification will ensure that the function returns the correct version without any additional text.