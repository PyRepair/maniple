The bug in the `info` function is due to the incorrect command used to get the Fish shell version. The function is currently trying to fetch the Fish shell version by executing `fish -c 'echo $FISH_VERSION'` but the test is asserting against the output of `fish --version`, which is different.

To fix this bug, we need to update the command in the `Popen` call to `fish --version` so that it matches the expected output in the test.

Here is the corrected version of the `info` function:

```python
# The corrected version of the info function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will return the Fish shell version parsed from the output of `fish --version`, which matches the expected output in the failing test.

This corrected version of the `info` function should now pass the failing test with the expected input/output values.