### Error Location:
The bug lies in the `info` function within the `fish.py` file. The issue is related to how the version string is extracted and formatted.

### Bug Explanation:
The `info` function in the buggy code is attempting to extract the Fish Shell version using the command `echo $FISH_VERSION`. However, in the failing test, the expected output is `'3.5.9'` while the actual output includes the text `'fish, version 3.5.9'`. This discrepancy causes the test to fail.

The discrepancy arises from using the incorrect command to retrieve the Fish Shell version, leading to extra text in the output that is not expected.

### Bug Fix Strategy:
To fix the bug, we need to update the command used to extract the Fish Shell version to eliminate the extra text. By modifying the command to only extract the version number, we can align the actual output with the expected output.

### Corrected Code:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With this fix, the function should now correctly extract just the version number from the output of `fish --version`, aligning it with the expected output in the failing test.