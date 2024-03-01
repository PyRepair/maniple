The bug in the `info` function lies in the command used to fetch the Fish shell version. The command `echo $FISH_VERSION` should be replaced with `fish --version` in order to correctly retrieve the Fish shell version.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By updating the command to fetch the Fish shell version, the corrected `info` function will now correctly return the version.