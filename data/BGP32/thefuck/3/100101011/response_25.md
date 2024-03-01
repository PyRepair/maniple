### Analysis:
1. The `info` function in the `shells/fish.py` file attempts to retrieve the Fish shell version by executing a command and capturing its output. However, the command used to get the version does not match with the expected output used in the test function.
2. The test function expects the version to be retrieved using `fish --version`, but the actual command used in the `info` function is `echo $FISH_VERSION`.
3. The discrepancy in the commands being used is causing the test to fail as the expected version output does not match the actual version output.
4. To fix the bug, the `info` function should use the correct command `fish --version` to retrieve the Fish shell version.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By updating the command to `fish --version`, the `info` function will now correctly retrieve the Fish shell version, matching the expectation in the test function, and solving the bug.