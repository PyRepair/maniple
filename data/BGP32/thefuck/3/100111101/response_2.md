### Bug Explanation:
The bug lies in the way the version is extracted from the output of the command `echo $FISH_VERSION`. The current implementation expects the output to be `4.5.9` but receives `fish, version 3.5.9`. This discrepancy causes the assertion failure.

### Fix Strategy:
To fix this bug, we need to modify the way we extract the version from the command output. Instead of expecting the output to be in a specific format, we should extract the version number from the output string. 

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(", version ")[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the version number is correctly extracted from the output, and the function should now return `'Fish Shell 3.5.9'` as expected in the test.