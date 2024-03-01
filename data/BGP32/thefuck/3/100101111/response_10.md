The bug in the `info` function arises from the incorrect command used to retrieve the Fish shell version. The Popen command should be passing `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to ensure that the version is correctly extracted.

The cause of the bug can be attributed to the incorrect command used to fetch the Fish shell version. The current implementation of the `info` function retrieves the version by running the command `echo $FISH_VERSION`, which is problematic. This leads to the test failing as it expects the version to be retrieved using the `--version` flag.

To fix this bug, we need to modify the command passed to the Popen call to `['fish', '--version']` to ensure that the correct Fish shell version is obtained.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Parsing the version to get the numeric part only
    version = version.replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly retrieve the Fish shell version using the `--version` flag, and the test case provided should now pass successfully.