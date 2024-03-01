### Analysis:
1. The buggy function `info` in the `Fish` class is attempting to retrieve the version of Fish Shell by executing a command using `Popen`, but it's failing because the returned version string includes more than just the version number.
2. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
3. The cause of the bug is that the function is not correctly parsing the version number from the output of the command executed.
4. To fix this bug, we need to extract only the version number from the output by modifying the way we extract the version from the `proc.stdout.read()`.
5. We need to update the `info` function to extract and format the version correctly.

### Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

By splitting the output based on spaces and taking the last element, we can extract just the version number. This fix should now correctly extract the version number and output `'Fish Shell 3.5.9'`.