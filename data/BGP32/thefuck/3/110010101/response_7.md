### Analysis
- The `info` function is intended to return the name and version of the current shell, which is Fish.
- The function calls the `Popen` function to run a command `echo $FISH_VERSION`, expecting to retrieve the Fish version.
- The test failure indicates that the returned value includes unwanted characters, specifically `'fish, version'` prefixing the version number.
- This unwanted prefix causes the assertion error in the test.

### Bug
The bug lies in how the output from the command execution is being processed. The returned value still contains the prefix `'fish, version'`, which is not needed.

### Fix
To fix this bug, we can modify the way we extract the version number to remove the prefix `'fish, version'`.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_with_prefix = proc.stdout.read().decode('utf-8').strip()
        version = version_with_prefix.split(' ')[-1]
        return u'Fish Shell {}'.format(version)
``` 

By splitting the returned value at whitespace and extracting the last element, we can get just the version number without the unwanted prefix. This corrected version of the function should now pass the failing test.