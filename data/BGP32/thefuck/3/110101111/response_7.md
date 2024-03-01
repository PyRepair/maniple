To fix the buggy function `info` in the `Fish` class, we need to update the command passed to `Popen` to correctly fetch the Fish shell version. The current command `['fish', '-c', 'echo $FISH_VERSION']` is incorrect as it does not return the version string in the expected format.

To resolve the bug:
1. Modify the command passed to `Popen` to `['fish', '--version']` to get the version information directly.
2. Update the decoding and formatting of the version string to extract just the version number.

Here is the corrected version of the `info` function in the `Fish` class:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extracting just the version number
        return u'Fish Shell {}'.format(version)
```

The new implementation ensures that the correct command is used to fetch the Fish shell version, and then extracts only the version number from the output.

This fix should resolve the issue mentioned in the GitHub post related to the Oh-My-Fish plugin and prevent the recursive loop triggered by the incorrect version fetching in the `info` function.