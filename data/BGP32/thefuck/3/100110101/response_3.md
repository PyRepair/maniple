The bug in the `info` function is caused by the incorrect command being used to retrieve the version of the Fish shell. The command used is `echo $FISH_VERSION`, but the test is expecting the version to be retrieved using `fish --version` instead.

To fix the bug, the command in the Popen call should be changed to `['fish', '--version']` to align with the test expectations.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly retrieve the version of the Fish shell using `fish --version` and return the expected output.