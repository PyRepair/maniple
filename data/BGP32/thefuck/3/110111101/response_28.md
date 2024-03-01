The bug in the provided function `info` lies in the way it retrieves the version information. The function is currently using the command `echo $FISH_VERSION` to obtain the version of the Fish shell. However, the expected version information is different than what is actually being retrieved, leading to the failing test.

The failing test specifies that the expected version is `'Fish Shell 3.5.9'`, but the actual version information retrieved from the command is `'fish, version 3.5.9'`. This difference in format causes the assertion error during the test.

To fix this bug, we need to modify the command used to retrieve the version information so that it matches the expected format.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

By changing the command from `echo $FISH_VERSION` to `fish --version`, we ensure that the version information retrieved matches the expected format. Additionally, we extract only the version number from the output using `.split(' ')[2]` to accurately get the version number without any extra characters.

This corrected version of the function should now pass the failing test and return the expected output `'Fish Shell 3.5.9'`.