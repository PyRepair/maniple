### Analysis:
1. The `info` function is calling `fish -c 'echo $FISH_VERSION'` to get the Fish Shell version.
2. The test function is setting the return value to `b'fish, version 3.5.9\n'` but expecting the output to be `'Fish Shell 3.5.9'`.
3. The error message indicates that the actual output includes unwanted characters (`fish, version`) causing the assertion to fail.
4. The GitHub issue mentions a recursive loop due to the use of `thefuck -v` in Oh-My-Fish plugin with a reference to fixing it.

### Bug Cause:
The bug is caused by the discrepancy between the expected output ('Fish Shell 3.5.9') and the actual output ('fish, version 3.5.9') due to the command used in the `info` function.

### Fix Strategy:
1. Modify the command in the `info` function to correctly extract the version without unnecessary text.
2. Update the test function to expect the correct output format.
3. Ensure that the fix aligns with the resolution mentioned in the GitHub issue regarding the recursive loop.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

In the corrected version, the command used to get the version has been changed to `['fish', '--version']`, and the output is correctly extracted without unwanted text. This change aligns with fixing the bug and resolves the failing test as expected.