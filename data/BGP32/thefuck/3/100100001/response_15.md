The bug in the `info` function arises from two main issues:
1. The Popen command is looking for the output of `echo $FISH_VERSION`, but the test is expecting the version output from `fish --version`.
2. The test is setting the side effect for `Popen.return_value.stdout.read` to return the version output, but the function is trying to read from `proc.stdout`.

To fix the bug, we need to update the Popen command to get the version using `fish --version` and read from `proc.stdout`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1].strip())
```

With this fix, the function will correctly get the version of the Fish shell using `fish --version` and return it. This updated version of the function should pass the failing test successfully.