The issue in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` used in the `Popen` call is trying to print the `FISH_VERSION` environment variable, whereas the test is expecting the Fish shell version to be obtained using `fish --version`.

To fix this bug, we need to modify the command in the `Popen` call to `['fish', '--version']` so that it aligns with the test expectation.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2][:-1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will execute the correct command to fetch the Fish shell version, and it should now pass the failing test.