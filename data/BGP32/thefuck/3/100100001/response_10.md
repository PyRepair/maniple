The bug in the `info` function is that it is using the command `echo $FISH_VERSION`, but the test is expecting the version to be retrieved using the command `fish --version`. This is why the test fails. To fix this bug, we need to update the command being executed in the `Popen` call to `['fish', '--version']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the `Popen` call now executes `fish --version` to retrieve the correct version information from the shell. This change aligns with the expectation in the test function, which verifies that the output matches 'Fish Shell 3.5.9' and that the command `['fish', '--version']` is called.

After applying this fix, the test should pass successfully.