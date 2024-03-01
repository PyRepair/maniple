The bug in the `info` function is due to the difference between the command used to retrieve the Fish shell version (`echo $FISH_VERSION`) and the command expected in the test (`fish --version`). This leads to the test failing as it doesn't match the expected command output.

To fix this bug, we need to modify the command used to fetch the Fish shell version to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

In this corrected version, we are running the correct command to get the Fish shell version (`fish --version`) which aligns with the expected output in the test. Additionally, we extract only the version number from the command output for consistent comparison with the expected output in the test.