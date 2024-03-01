The issue with the `info` function in the `Fish` class is that it is trying to get the Fish shell version by running `echo $FISH_VERSION` but the test is expecting the version to be extracted from the output of `fish --version`. This mismatch results in the failing test.

To fix this bug, we need to update the command in the `Popen` call to `fish --version` instead of `echo $FISH_VERSION`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract version number
    return u'Fish Shell {}'.format(version)
```

With this correction, the function now correctly fetches the version of the Fish shell through `fish --version`, matching the expectations of the failing test.