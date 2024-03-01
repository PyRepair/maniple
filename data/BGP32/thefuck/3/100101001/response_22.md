### Fixing the bug

The bug in the `info` function stems from the fact that the command used to retrieve the Fish shell version is incorrect. The command `'echo $FISH_VERSION'` is being used, but the test is expecting the output of `'fish --version'`.

To fix this bug, the function should be updated to run the correct command to retrieve the version information of the Fish shell.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

This correction addresses the issue by running the command `'fish --version'` to obtain the correct version information of the Fish shell.