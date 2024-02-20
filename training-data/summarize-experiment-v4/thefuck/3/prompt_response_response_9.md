## Bug's Cause

The bug is caused by the use of an incorrect command to retrieve the version of the Fish shell in the `info` function. The `Popen` call with the command `['fish', '-c', 'echo $FISH_VERSION']` does not return the expected output, causing the failed assertion in the test.


## Fixing the Bug

To fix the bug, the correct command to retrieve the version of the Fish shell needs to be utilized in the `Popen` call. This command should directly output the version string without additional text.

The corrected code for the `info` function is as follows:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '-v']`, the correct version information is obtained from the Fish shell.

This fix addresses the incorrect command used to retrieve the Fish shell version, ensuring that the expected output matches the actual output and resolving the issue posted on GitHub.