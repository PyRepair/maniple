The bug in the `info` function is caused by using the incorrect command `echo $FISH_VERSION` instead of `fish --version` which leads to the wrong output and consequently fails the test.

To fix this bug, we need to update the command used in the `Popen` call to `['fish', '--version']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[2])
```

By updating the command to `['fish', '--version']`, the function now correctly retrieves the version information and provides the expected output.