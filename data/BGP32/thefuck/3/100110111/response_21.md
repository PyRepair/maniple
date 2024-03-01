## Analysis
1. The buggy function `info` is attempting to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected version is '3.5.9', and this discrepancy causes the assertion error.
2. The `Popen` function is used to execute the command and capture the output, but the command being executed doesn't match the expected command in the test.
3. The assertion fails because the actual output includes more text than just the version number. It contains "fish, version 3.5.9\n" instead of only '3.5.9'.
4. To fix the bug, we need to modify the command being executed to `['fish', '--version']` to match the expected output in the test.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_line = proc.stdout.readline().decode('utf-8').strip()
    version = version_line.split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the `info` function will execute the `['fish', '--version']` command to get the version information, extract the version number from the output, and return it in the expected format. This fix aligns the function behavior with the test expectations and resolves the assertion error.