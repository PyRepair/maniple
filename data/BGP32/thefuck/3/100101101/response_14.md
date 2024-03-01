The bug in the provided function `info` is due to the incorrect command used to retrieve the Fish shell version. The function is currently executing `fish -c 'echo $FISH_VERSION'` to get the version, but the test code expects the version to be fetched using `fish --version`.

To fix this bug, we need to update the command used to get the Fish shell version in the `info` function. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, the function will now correctly retrieve the Fish shell version. The function also includes additional parsing to extract just the version number.

This updated version should pass the failing test case provided.