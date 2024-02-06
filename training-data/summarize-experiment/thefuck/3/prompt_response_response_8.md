The issue with the current `info` function is that it is using the wrong command to retrieve the Fish Shell version. The command `fish -c 'echo $FISH_VERSION'` is incorrect and should be replaced with `fish --version` to retrieve the correct version information.

To fix the bug, we need to update the command used in the `Popen` call within the `info` function.

Here's the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
```

The issue of using the incorrect command has been addressed by updating the `Popen` call to use the correct command `['fish', '--version']`. This change ensures that the function retrieves the correct version information for the Fish Shell.

This corrected code can be used as a drop-in replacement for the buggy version of the function.