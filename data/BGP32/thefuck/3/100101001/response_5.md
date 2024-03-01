The bug in the function `info` is due to the incorrect command used to retrieve the version of the Fish shell. The command `echo $FISH_VERSION` is being used, but the test is expecting the version to be retrieved using the command `fish --version`.

To fix the bug, we need to update the command being executed to get the version of the Fish shell. We should change `echo $FISH_VERSION` to `fish --version`.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[2])
```

This corrected version uses the correct command `fish --version` to retrieve the version of the Fish shell.