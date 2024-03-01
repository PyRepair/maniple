The cause of the bug in the provided function `info` is that the command used to get the Fish shell version is incorrect. The command `['fish', '-c', 'echo $FISH_VERSION']` is trying to echo the variable `$FISH_VERSION`, but the correct command to get the version of Fish shell is `['fish', '--version']`.

To fix the bug, we need to update the command in the `Popen` call to `['fish', '--version']`. This will ensure that the correct version of the Fish shell is captured and returned by the `info` function.

Here is the corrected version of the function `info`:

```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will now properly capture the version of Fish shell and return it in the specified format. The provided failing test should now pass with this corrected version of the function.