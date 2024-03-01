## Correction:

The bug in the `info` function lies in the fact that it is trying to retrieve the Fish shell version using the command `echo $FISH_VERSION` instead of the correct command `fish --version`. This results in the version string containing unwanted information which causes the test to fail.

To fix this bug, we need to update the command used to get the Fish shell version. Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now correctly extract the version information and pass the failing test.