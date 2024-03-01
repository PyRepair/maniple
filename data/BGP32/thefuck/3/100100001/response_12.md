The bug in the `info` function is caused by passing `['fish', '-c', 'echo $FISH_VERSION']` as the command to retrieve the version of the Fish Shell. However, in the failing test, it is expected that the command `['fish', '--version']` should be called to get the version information.

To fix this bug, we need to update the command used to retrieve the Fish Shell version in the `info` function. The command should be changed from `['fish', '-c', 'echo $FISH_VERSION']` to `['fish', '--version']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[2])
```

In this corrected version, we use `['fish', '--version']` to get the version information, and then extract the version number from the output using `split()[2]` to format it as `Fish Shell x.x.x`.

After making this change, the corrected version of the `info` function should pass the failing test.