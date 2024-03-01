The bug in the `info` function of the `Fish` class lies in the command used to retrieve the Fish shell version. The current command `echo $FISH_VERSION` is incorrect as it only outputs the literal string "$FISH_VERSION" instead of the actual version number. This causes the function to return a string with the literal version command and not the actual version number.

To fix this bug, the command used to retrieve the Fish shell version should be changed to `fish --version` so that the correct version number is obtained.

Here is the corrected version of the `info` function:

```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return f'Fish Shell {version}'
```

This corrected version of the function will successfully extract the version number using the correct command, `fish --version`, and return the actual version number as expected.