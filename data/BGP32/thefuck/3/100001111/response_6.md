The bug in the `info` method of the `Fish` class is due to the incorrect parsing of the version output from the command `echo $FISH_VERSION`. The code expects the output to be `'fish, version x.y.z'`, however, it actually returns `'x.y.z'`. This discrepancy causes the bug as the version string is not extracted correctly.

To fix this bug, we need to modify how the version string is extracted. We can simply split the output of the command by spaces and take the last element as the version number.

Here is the corrected version of the `info` method:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

This corrected version should now correctly extract the version number from the output of the `echo $FISH_VERSION` command and return it along with the shell name.