Based on the information provided, the bug in the `info` function in the `Fish` class is due to the incorrect command being passed to Popen and reading the wrong value for the Fish shell version.

### Analysis:
1. The current command passed to Popen is `['fish', '-c', 'echo $FISH_VERSION']`, which is different from the expected `['fish', '--version']` in the failing test.
2. The expected version string in the failing test is `'fish, version 3.5.9'`, but the code is trying to read and format the version incorrectly.

### Bug Cause:
The bug is caused by using the wrong command argument and not reading the correct version string from the output, leading to a mismatch between the actual version and the expected version in the test.

### Fix Strategy:
1. Update the command passed to Popen to `['fish', '--version']`.
2. Modify the reading and formatting of the version string to match the expected format.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version_bytes = proc.stdout.read()
        # extract version string from bytes and decode
        version = version_bytes.decode('utf-8').strip()
        # split the version string to get just the version number
        version_parts = version.split(', version ')
        if len(version_parts) > 1:
            version_number = version_parts[1]
        else:
            version_number = version
        return f'Fish Shell {version_number}'
```

By making these changes, the `info` function should now correctly fetch the Fish shell version and format it according to the expected output. This corrected version should pass the failing test mentioned above and resolve the issue posted on GitHub.