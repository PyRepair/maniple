The bug in the `info` function is due to the wrong command being used to get the Fish version (`echo $FISH_VERSION` instead of `fish --version`). This causes the version to be read incorrectly, leading to the mismatch in the test assertion.

To fix the bug, we need to update the command used to get the Fish version in the `info` function.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

By updating the command to `['fish', '--version']`, we ensure that the version string is extracted correctly. The corrected function should now pass the failing test case.