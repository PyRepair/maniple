Based on the information provided, the bug in the `info` method of the `Fish` class seems to be related to the command being executed using the `Popen` function and how the output is being read. 

The command being executed `'fish -c 'echo $FISH_VERSION'` is incorrect. It should be `['fish', '--version']` to obtain the version of the Fish Shell.

To fix the bug, the following changes should be made to the `info` method:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function will ensure that the correct version information is obtained from the Fish Shell, resolving the bug. The output can be used as a drop-in replacement for the original buggy version of the function.