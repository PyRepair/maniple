The bug in the `info` function is caused by the fact that it is capturing the output of `echo $FISH_VERSION`, but the test is expecting `--version` instead. This discrepancy causes the version check to fail.

To fix this bug, we need to update the command passed to `Popen` in the `info` function to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`. 

Here is the corrected version of the `info` function:

```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```

This corrected version will correctly retrieve and format the version number from the output of `fish --version` and return 'Fish Shell 3.5.9'.

With this correction, the failing test provided should now pass without any assertion errors.