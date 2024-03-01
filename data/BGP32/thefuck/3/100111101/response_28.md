The bug in the `info` function is caused by the incorrect command used to retrieve the Fish shell version. Instead of using `echo $FISH_VERSION`, the correct command should be `fish --version`. This leads to the unexpected output format, causing the test to fail.

To fix the bug, the command used to get the Fish shell version should be updated to `fish --version`.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function now correctly extracts the version number from the output of the `fish --version` command, and the test should pass successfully.