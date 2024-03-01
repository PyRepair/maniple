### Analysis:
1. The buggy function `info` in the `Fish` class is attempting to retrieve the Fish shell version using the `echo $FISH_VERSION` command. However, the function is not correctly parsing the output to extract just the version number.
2. The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output contains additional text `"fish, version"` before the version number.
3. The erroneous behavior could be due to not properly decoding the output or failing to strip extra characters before constructing the final version string.
4. To fix the bug, the function needs to correctly extract and format the version number from the output of the `echo $FISH_VERSION` command.

### Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.replace("fish, version", "").strip()  # Remove extraneous text
        return f'Fish Shell {version}'
```

After applying this fix, the `info` function should correctly extract the version number and return `'Fish Shell 3.5.9'` as expected, resolving the failing test case.