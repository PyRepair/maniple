The bug in the `info` function lies in the way it retrieves the version of the Fish shell. It is using the command `echo $FISH_VERSION` to get the version, but the test is expecting the version to be retrieved using `fish --version`.

### Cause of the bug:
The `info` function is not executing the correct command to retrieve the Fish shell version. This mismatch in the command used for version retrieval causes the failing test since the expected version format is different.

### Strategy to fix the bug:
To fix the bug, the `Popen` command should be updated to execute `fish --version` instead of `echo $FISH_VERSION` to retrieve the correct version format that matches the expectations of the test.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(' ')[-1])
```

By updating the command to `fish --version` in the `Popen` call, the function will retrieve the Fish shell version in the expected format, allowing it to pass the failing test.