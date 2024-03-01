### Analysis
1. The `info` function in the `Fish` class is attempting to extract the version of the Fish shell by running a command in the shell.
2. The test case is mocking the response of the `Popen` call to simulate the output of the `fish --version` command.
3. The error occurs because the assertion is comparing the full string returned by the `info` function with the expected string, which includes unnecessary text.
4. To fix the bug, we need to modify the parsing logic to extract only the version number from the output.

### Bug Fix Strategy
1. Update the code in the `info` function to correctly parse and extract only the version number from the output of the command.
2. Modify the test case to match the updated logic of the `info` function.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

Make sure to update the test file accordingly to reflect the changes made in the corrected version of the `info` function.