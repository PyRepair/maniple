The bug in the `info` function stems from the fact that the command used to get the Fish shell version in the `Popen` call is incorrect. The command should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

### Strategy for fixing the bug:
- Update the `Popen` call to use `['fish', '--version']` to correctly fetch the Fish shell version.

### Corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By using the corrected version of the `info` function above, the tests should now pass successfully.