### Bug Explanation
The bug in the `info` function arises from two main issues:
1. The command being executed to get the version of Fish shell is `'echo $FISH_VERSION'` instead of `'fish --version'`.
2. The comparison in the test function is failing because the actual output obtained includes additional text `'fish, version 3.5.9'` while the expected output is `'Fish Shell 3.5.9'`.

### Fix Strategy
To fix the bug:
1. Modify the command in the Popen call to `'fish --version'` to correctly retrieve the version of Fish shell.
2. Adjust the expected output format to match the actual output by removing the additional text `'fish, '`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, ', '')  # Remove unnecessary text
    return 'Fish Shell {}'.format(version)
``` 

After making these changes, the function should correctly obtain the version of the Fish shell and return it in the expected format. This fixed version should pass the failing test.