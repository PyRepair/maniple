The bug in the `info` function is caused by the incorrect command used to fetch the Fish shell version, as well as the incorrect way of reading the output of the command.

To fix the bug:
1. Update the command in the `Popen` call to use `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'` to retrieve the version information.
2. Modify the way of reading the output of the command to properly decode it and extract the version number.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

This corrected version should now pass the failing test case provided.