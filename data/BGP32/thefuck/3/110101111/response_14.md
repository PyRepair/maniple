The buggy function `info()` in the `Fish` class is not correctly retrieving the Fish shell version from the command line output. The issue originates from the incorrect command being used to capture the version information.

Here's the analysis and the corrected version:

### Analysis:
1. The `info()` function in the `Fish` class is supposed to return the name and version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`.
2. The failing test sets up the `Popen` return value to simulate the command output, but the expected version format is `'3.5.9'`, not `'fish, version 3.5.9'`.
3. The function is currently extracting the version directly without removing the unnecessary text.

### Bug Cause:
The `info()` function is not correctly parsing the version information from the command output, leading to a mismatch with the expected output in the test case.

### Bug Fix Strategy:
1. Update the command in `Popen` to retrieve the version in a proper format.
2. Modify the code to extract and format the version string correctly before returning it.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(', version ')[1]
        return f'Fish Shell {version}'
```

With this corrected version, the function will run the appropriate command to get the shell version and parse it correctly. This updated code should now pass the failing test case and provide the expected output.