The test function `test_info` is asserting that the output of `shell.info()` should be 'Fish Shell 3.5.9', but the actual output is 'Fish Shell fish, version 3.5.9'. 

The issue is within the `info` function. The `Popen` call is using the wrong command to get the Fish shell version, and the format string used to construct the return value is also incorrect.

The reason for the bug is that the `Popen` call uses the command `fish -c 'echo $FISH_VERSION'` which only returns the version number without any label. Additionally, the return value is being formatted with 'Fish Shell {}'.format(), but the actual version number returned is prefixed with 'fish, version'. 

To fix the bug, we need to modify the command passed to `Popen` and also update the format string used for constructing the return value.

Here's the corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

This revised function uses the correct command `fish --version` to get the Fish shell version, and then extracts the version number from the output and constructs the return value in the expected format.

By using this corrected function, the test `test_info` should pass without any assertion errors.