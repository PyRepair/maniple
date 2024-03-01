### Analysis:
- The buggy function `info` in the `Fish` class is supposed to return the name and version of the current Fish shell.
- The failing test `test_info` is expecting the output of the `info` function to be `'Fish Shell 3.5.9'`.
- The error message indicates that the output is actually `'Fish Shell fish, version 3.5.9'`, leading to an assertion error.
- This discrepancy suggests that the parsing of the version string from the shell command output is incorrect in the `info` function.

### Bug Cause:
- The bug is caused by incorrectly parsing the output of the `echo $FISH_VERSION` command in the `Fish` class `info` method.
- The version string contains extra text `fish,` before the actual version number, causing the assertion to fail.

### Bug Fix:
- To fix the bug, we need to update the parsing logic to extract only the version number from the output.
- We can use string manipulation techniques to extract the version number from the output.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(', version ')[1]  # Extract version number
        return 'Fish Shell {}'.format(version)
```

By updating the parsing logic to extract the version number correctly, the corrected version of the function should now return the expected output and pass the failing test.