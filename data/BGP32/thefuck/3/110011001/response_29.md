### Analysis
- The `info` function is attempting to get the version of the Fish shell by executing a command in the shell and capturing the output.
- The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
- This discrepancy suggests that the `version` variable is not being extracted correctly from the command output.
- The issue seems to be related to how the command output is being read and processed.

### Bug Fix Strategy
- The problem lies in how the output of the `Popen` command is being read and decoded to get the version number.
- We need to ensure that we extract the correct version number from the command output without including the unnecessary prefix `'fish, version'`.
- To fix this bug, we should modify the way we process the `version` variable to only include the version number.

### Corrected Version
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')  # Fix: Extract only the version number
        return u'Fish Shell {}'.format(version)
```