### Analysis:
The buggy function is attempting to retrieve the version of the current Fish shell by executing a command using Popen and capturing the output. The bug lies in the fact that the command being executed is not correct, leading to the incorrect version being retrieved.

### Error Cause:
1. The command `echo $FISH_VERSION` in the Popen call does not retrieve the version correctly, resulting in the 'fish, version 3.5.9' string instead of just '3.5.9'.
2. The assertion in the test function expects 'Fish Shell 3.5.9' but receives 'Fish Shell fish, version 3.5.9'.

### Fix Strategy:
1. Modify the Popen command to retrieve the version correctly without the extra text.
2. Update the assertion in the test to match the corrected version retrieval.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```