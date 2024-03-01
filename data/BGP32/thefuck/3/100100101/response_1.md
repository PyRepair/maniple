### Fixing the Bug
The bug in the `info()` function is caused by the incorrect command used to retrieve the Fish shell version. The command used is `'echo $FISH_VERSION'` which does not provide the correct version string. The correct command should be `'fish --version'` to retrieve the version information.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By updating the command to `'fish --version'`, the function will correctly retrieve the version information of the Fish shell and return it in the expected format.

This corrected function will pass the failing test provided.