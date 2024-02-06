The buggy function `info` is intended to return the name and version of the current Fish shell. However, the bug lies in the `Popen` function call, where the command being executed is incorrect. It should be `fish --version` instead of `fish -c 'echo $FISH_VERSION'`.

To fix this bug, the `Popen` command inside the `info` function should be changed to `['fish', '--version']`. Additionally, the output from the `Popen` call should be properly read and decoded to obtain the version information.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.communicate()[0].decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this fix, the `Popen` command executes `fish --version` to correctly obtain the version information. The output from the `Popen` call is now obtained using `proc.communicate()[0].decode('utf-8').strip()` to properly capture and decode the version information.

This revised version of the function can be used as a drop-in replacement for the buggy version.