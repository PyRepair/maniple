### Analysis
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and capturing the output. However, the test case is expecting the version string `3.5.9` directly from the command output.
2. The error message shows that the actual output includes the additional text "fish, version" before the version number.
3. The cause of the bug is that the code is directly reading the output without considering the exact format returned by the command.
4. To fix the bug, we need to modify the code to extract and format the version number correctly from the command output before constructing the final string.

### Bug Fix Strategy
1. Modify the `info` function to correctly extract the version number from the command output.
2. Update the test case to ensure it matches the expected behavior with the fixed function.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.replace("fish, version ", "")
        return 'Fish Shell {}'.format(version)
```

By modifying the code to extract the version number correctly before constructing the final string, the corrected version of the function should pass the failing test.