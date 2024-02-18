The bug in the `info` method of the Fish shell class is caused by the incorrect command used to retrieve the version of the Fish shell. The current implementation is using the command `echo $FISH_VERSION` which returns 'fish, version 3.5.9' instead of the expected '3.5.9'. This causes the test case to fail with an AssertionError due to the mismatch between the expected and actual output.

To fix this bug, the `Popen` function should be used to execute the command `fish --version` which will return the correct version of the Fish shell. This will ensure that the `info` method returns the expected version of the shell.

Here is the corrected code for the `info` method:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Splitting the version to get only the version number
    version = version.split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

With this change, the `info` function will now correctly obtain the version of the Fish shell and return it in the expected format. This fixes the bug and ensures that the failing test case is resolved.