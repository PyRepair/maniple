The bug in the provided function `info` lies in the command used to retrieve the version of the Fish shell. The command `echo $FISH_VERSION` is incorrect, as it does not output the version number in the desired format.

To fix this bug, the command should be changed to `fish --version` to correctly obtain the version of the Fish shell.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[2] if version else ""
    return 'Fish Shell {}'.format(version)
```

This corrected version of the function should now return the version of the Fish shell in the correct format, resolving the bug and passing the failing test case provided.