The bug in the function `info` is caused by the incorrect command `'echo $FISH_VERSION'` being used to retrieve the Fish Shell version. This command does not provide the version number directly, resulting in the incorrect output in the failing test. 

To fix the bug, we need to change the command to `'fish --version'` to correctly fetch the Fish Shell version. 

Below is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[2]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will now correctly extract the Fish Shell version and pass the failing test case.