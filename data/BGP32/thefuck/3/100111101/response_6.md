The bug in the `info` function arises from not using the correct command to fetch the Fish shell version. The function is using `echo $FISH_VERSION` while the test expects the version to be extracted from the output of `fish --version`. This discrepancy causes the function to return the incorrect version format.

To fix this bug, we need to update the command in the `Popen` call to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

By making this change, the function now correctly fetches the version from the output of `fish --version`, which aligns with the expectations of the test.