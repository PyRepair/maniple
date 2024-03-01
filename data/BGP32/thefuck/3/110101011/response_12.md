The bug in the `info` function of the `Fish` class is caused by the incorrect command used to get the Fish version (`echo $FISH_VERSION` instead of `fish --version`). This leads to incorrect parsing of the version information, causing the test to fail.

To fix this bug, we need to update the command to get the Fish version correctly.

Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(",")[1].strip())
```

By updating the command to `['fish', '--version']`, we ensure that the correct version information is obtained from the shell. Additionally, we parse the output to extract only the version number to match the expected output in the test.

With this correction, the `info` function should now return the correct Fish Shell version, passing the failing test.