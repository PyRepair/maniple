The bug in the `info` function is caused by the incorrect command used to get the Fish shell version. The command `echo $FISH_VERSION` is retrieving the value of the environment variable `FISH_VERSION`, which may not be set, resulting in an empty response. This leads to the `version` variable being empty and causing the assertion to fail.

To fix this bug, we should modify the command to directly get the Fish shell version by using `fish --version` instead of `echo $FISH_VERSION`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This correction should now correctly fetch the Fish shell version using `fish --version`, resolving the bug and allowing the failing test to pass successfully.