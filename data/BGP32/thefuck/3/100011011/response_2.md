## Identify the bug
The bug in the `info` function lies in how it retrieves the Fish Shell version. The current approach using `echo $FISH_VERSION` is incorrect as it includes additional text that causes the generated version string to be incorrect.

## Explanation of the bug
The failing test provides the expected output as `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This discrepancy is due to the fact that the command `echo $FISH_VERSION` returns a string with additional text (`fish, version`), which is not part of the version number.

## Fix strategy
To fix the bug, we need to modify the command used to retrieve the Fish Shell version to only extract the version number without any additional text.

## Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By changing the command from `echo $FISH_VERSION` to `echo $version`, we ensure that only the version number is extracted, resolving the bug and aligning the function output with the expected result.