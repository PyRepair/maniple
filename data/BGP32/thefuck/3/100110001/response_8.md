## Analysis
1. The `info` function in the `Fish` class of `fish.py` is attempting to retrieve the version of Fish shell by running `echo $FISH_VERSION` command.
2. The failing test is trying to assert that the version returned by the `shell.info()` function is equal to the expected version `'Fish Shell 3.5.9'`.
3. The error message shows that the actual version returned by `shell.info()` is `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
4. The incorrect version is due to the fact that the command being run in the `info` function does not output `FISH_VERSION` in the correct format for parsing.

## Bug
The bug arises from the fact that the command `echo $FISH_VERSION` does not directly output just the version number of Fish shell. As a result, the function fails to extract the version number correctly.

## Fix Strategy
1. Since the `FISH_VERSION` environment variable may not directly give us the version number, we need to adjust the command to get the version number in a reliable format.
2. Change the command to `fish --version` to retrieve the version of the Fish shell directly.
3. Strip the extra text returned by the command to get only the version number.

## Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_string = proc.stdout.read().decode('utf-8').strip()
    version = version_string.split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
``` 

With the above correction, the `info` function will correctly extract the version number using `fish --version` command, extract only the version from the text returned, and return `"Fish Shell version_number"` as expected.

The corrected function should now pass the failing test successfully.