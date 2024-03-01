### Analysis
The buggy function `info` is attempting to retrieve the version of Fish shell by running a subprocess. However, it reads the output from the subprocess incorrectly. The function assumes that `proc.stdout.read()` returns the output directly as a string, but in reality, it returns a `bytes` object.

### Bug Explanation
The bug occurs because the function is trying to decode a `bytes` object directly, resulting in an error when trying to format it using `u'Fish Shell {}'.format(version)`.

### Bug Fix Strategy
To fix the bug, we need to decode the `bytes` object returned by `proc.stdout.read()` before using it in the string formatting.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```