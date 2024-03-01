The bug in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. The current command `echo $FISH_VERSION` is incorrect as it outputs "fish, version 3.5.9" instead of just the version number.

To fix the bug, the command should be changed to `fish --version` to get the correct version output.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', ')[1])
```

This corrected version should now properly extract the version number from the output of the `fish --version` command.