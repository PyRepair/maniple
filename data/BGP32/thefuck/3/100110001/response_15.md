The bug in the provided function `info()` is that it is trying to fetch the version of Fish shell using the command `echo $FISH_VERSION`, but the test is mocking the output of `fish, version 3.5.9` for the `--version` command. This mismatch is causing the test to fail.

To fix this bug, we need to update the command used in the `Popen` call to fetch the Fish shell version compatible with the expected value in the test. 

Here is the corrected version of the `info()` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return f'Fish Shell {version}'
```

In the corrected version, we are using the `--version` command to fetch the version of Fish shell, and then splitting the output to extract only the version number. This will ensure that the output format aligns with the expected value in the test.

After applying this fix, the `info()` function should now correctly fetch the version of Fish shell based on the `--version` command and pass the provided failing test.