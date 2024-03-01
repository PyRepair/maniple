### Analysis
The bug in the `info` function stems from the fact that the returned version string includes unnecessary text. The function is returning "Fish Shell fish, version 3.5.9" instead of "Fish Shell 3.5.9".

### Bug Cause
- The bug occurs because the function is directly returning the output of the command without filtering out the unnecessary text like "fish, version".

### Fix Strategy
- To fix the bug, we need to extract only the version number from the output of the command and return it in the correct format.

### The corrected version of the function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
        return u'Fish Shell {}'.format(version)
``` 

After applying this fix, the function should correctly return "Fish Shell 3.5.9" as expected.