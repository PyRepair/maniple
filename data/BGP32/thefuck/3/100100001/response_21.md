The bug in the provided code is in the call to Popen where the command passed is 'fish -c echo $FISH_VERSION' instead of 'fish --version'. This results in the incorrect retrieval of the version information from the Fish shell. To fix this bug, the command passed to Popen should be corrected to 'fish --version'.

Here is the corrected version of the buggy function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will execute 'fish --version' to get the correct version information of the Fish shell, leading to correct output and passing the failing test.