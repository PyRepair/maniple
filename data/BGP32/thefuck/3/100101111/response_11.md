### Bug Analysis
1. The `info` function in `fish.py` is using the command `'echo $FISH_VERSION'` to get the version of Fish shell, but the expected version is retrieved using `'fish --version'`.
2. The test is expecting the version number directly from the `--version` command output, so the current implementation is incorrect.
3. The mock values in the failing test and the actual values in the function during runtime are mismatched.
4. The incorrect command in the function causes the test to fail.

### Bug Fix Strategy
To fix the bug:
1. Update the command in the `Popen` call to `['fish', '--version']` to match the expected version output retrieved by the test.
2. Modify the function to extract and format the version correctly from the command output.
3. Ensure that the mocked return values align with the new command output format.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With the corrected function using the `--version` command, along with appropriate handling of the version extraction, the test should now pass successfully.