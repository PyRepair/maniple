### Analysis:
1. The buggy function `info` is attempting to retrieve the Fish shell version by executing a command and reading the output.
2. The error message indicates that the actual output `'fish, version 3.5.9'` is not matching the expected output `'Fish Shell 3.5.9'`.
3. The discrepancy in the output is due to the incorrect formatting of the version string retrieved from the command output. The function is returning `u'Fish Shell {}'.format(version)`, which is appending the `'Fish Shell'` prefix to the entire output string obtained from the command.
4. To fix the bug, we need to extract only the version number from the output string before formatting the final result.

### Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extract only the version number from the output string
        version_number = version.split(',')[1].strip()
        
        return u'Fish Shell {}'.format(version_number)
```

By extracting and formatting only the version number from the command output, the corrected function should now return the expected output `'Fish Shell 3.5.9'`.