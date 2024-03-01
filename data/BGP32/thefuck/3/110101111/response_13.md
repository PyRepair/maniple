### Identified Bug:
The `info` function in the `Fish` class is not correctly retrieving the version of the Fish shell due to an incorrect command `'echo $FISH_VERSION'` rather than `'fish --version'`. This causes the function to fail the test case and the GitHub issue.

### Bug Explanation:
1. The function uses `'echo $FISH_VERSION'` instead of `'fish --version'` to get the version of the Fish shell.
2. The test case expects the version to be extracted using `'fish --version'`.
3. As a result, the function returns a version string that includes unnecessary characters (e.g., `fish, version`). 

### Bug Fix Strategy:
Modify the command in the `Popen` function to `'fish --version'` in order to correctly extract the Fish shell version.

### Corrected Version:
```python
# The corrected version of the function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
```

By making this change, the function now correctly retrieves the version of the Fish shell using `'fish --version'`, and the corrected function should pass the failing test and resolve the GitHub issue.