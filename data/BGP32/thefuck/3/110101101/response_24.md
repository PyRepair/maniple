## Analysis
1. The buggy function `info()` is supposed to return the version of the Fish shell by running the command `echo $FISH_VERSION` in the shell process. However, the test case is expecting the version string to be `'Fish Shell 3.5.9'`, but the output of the shell command is `'fish, version 3.5.9'`.
2. The issue lies in the way the output of the `echo $FISH_VERSION` command is being processed in the `info()` function.
3. The function is not correctly formatting the version string and adding the prefix `'Fish Shell'`.
4. To fix the bug, we need to remove the unnecessary prefix `'Fish Shell'` from the version string before returning it.

## Bug Fix
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        fish_version = version.split(', version ')[-1]
        return fish_version
```

By splitting the version string based on `', version '`, we can extract the actual version number without the unnecessary prefix `'Fish Shell'`. This corrected version should pass the failing test case and return the expected output.