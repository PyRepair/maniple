The cause of the bug in the `info` function is that the command used to get the Fish shell version is incorrect. The command `echo $FISH_VERSION` does not provide the correct version output.

To fix this bug, we need to change the command used to get the Fish shell version. We should use `fish --version` instead of `echo $FISH_VERSION` to retrieve the correct version information.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
``` 

This corrected version should now correctly extract the Fish shell version using the `fish --version` command.