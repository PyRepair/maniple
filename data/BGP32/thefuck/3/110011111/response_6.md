### Identified Bug:
The bug in the `info` function of the `Fish` class is that the version string returned from the `proc.stdout.read()` call includes unwanted text (`'fish, version '`) along with the actual version number. This extra text is causing the assertion error during the test execution.

### Bug Cause:
- The `Popen` call with `['fish', '-c', 'echo $FISH_VERSION']` fetches the version information along with additional text.
- The `proc.stdout.read().decode('utf-8').strip()` call reads the output as `'fish, version 3.5.9'`.
- The assertion error occurs because the expected output is `Fish Shell 3.5.9` but the actual output contains the unwanted `'fish, version '` text.

### Fix Strategy:
Since the version string is prefixed with `'fish, version '`, we need to remove this unwanted text to obtain just the version number that matches the expected output.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_number = version.split(' ')[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version_number)
```

By splitting the version string based on spaces and extracting the last part of it, we effectively remove the unwanted `'fish, version '` text. This corrected version should now produce the expected output and pass the failing test.