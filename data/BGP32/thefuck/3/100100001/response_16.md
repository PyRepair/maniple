The bug in the `info` function lies in the command used to retrieve the version of the Fish shell. The command `fish -c 'echo $FISH_VERSION'` used in the `Popen` call does not actually return the version of the shell, causing the function to return incorrect results.

To fix the bug, we need to modify the command sent to the Fish shell to get the version information properly.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_parts = version.split()
    if len(version_parts) >= 2:
        version = version_parts[2]
    else:
        version = 'Unknown'
    return u'Fish Shell {}'.format(version)
```

With this modification, the correct version of the Fish shell should be retrieved, and the test should pass successfully.