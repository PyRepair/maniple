The issue in the `info` function arises from the command used to retrieve the version of Fish shell - 'echo $FISH_VERSION'. This command does not return the version directly, hence causing the version variable to be empty.

To fix this bug, the command should be changed to 'fish --version' which returns the version information directly.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[2])
``` 

With this correction, the function should now correctly extract the version from the output of 'fish --version', enabling it to pass the failing test.