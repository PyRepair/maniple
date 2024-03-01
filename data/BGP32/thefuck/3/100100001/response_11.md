The bug in the `info()` function arises from the fact that the command used to retrieve the Fish shell version is incorrect. The function uses `echo $FISH_VERSION` instead of `fish --version` to get the version information. This causes the function to retrieve an incorrect output, leading to a failure in the test case.

To fix this bug, we need to update the command passed to the Popen constructor to `fish --version` so that it correctly fetches the Fish shell version information.

Here is the corrected version of the `info()` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version.split()[-1])
```

With this correction, the function should now correctly retrieve the Fish shell version using the `fish --version` command instead of `echo $FISH_VERSION`, which will make the test case pass successfully.