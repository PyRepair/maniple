The issue in the provided function is that it is not properly handling the reading of the output from the subprocess. The `proc.stdout.read()` method is a one-time operation, meaning that once it is read, subsequent reads will return an empty string. This leads to the `version` variable being incorrect.

To fix this issue, we can modify the function to use the `communicate()` method of the subprocess instead of directly reading from the stdout. This method allows us to read both stdout and stderr and prevents the one-time read issue.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()`, we ensure that we capture all the output from the subprocess and correctly decode it to get the version value. This should fix the bug and return the correct version of the Fish Shell.