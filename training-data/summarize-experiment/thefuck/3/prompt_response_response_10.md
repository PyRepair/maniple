The test case `test_info` asserts that the output of `shell.info()` should be 'Fish Shell 3.5.9', but the actual output is 'Fish Shell fish, version 3.5.9'. This indicates that the function is not correctly extracting the version number from the shell command output.

The issue lies in the line `version = proc.stdout.read().decode('utf-8').strip()`. It seems that the command `echo $FISH_VERSION` is returning the entire string 'fish, version 3.5.9' instead of just the version number.

To fix this issue, we need to modify the command being executed to only return the version number.

The corrected code for the buggy function is:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

This code changes the command from `echo $FISH_VERSION` to `fish --version` to directly get the version information. Additionally, the `split()[-1]` method is used to extract the version number from the returned string. This should resolve the issue and provide the correct version number for the Fish shell.