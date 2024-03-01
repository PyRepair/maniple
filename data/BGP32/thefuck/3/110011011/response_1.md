### Analysis:
1. The buggy function `info(self)` in the `Fish` class attempts to retrieve the version of the Fish shell by executing a command in a subprocess.
2. The error message from the failing test indicates that the expected version string '3.5.9' is not matching with the actual version string returned by the function.
3. The runtime values show that the `version` variable contains the value `'fish, version 3.5.9'`, which includes additional unwanted text.
4. The GitHub issue suggests that the current implementation is causing a recursive loop when using the plugin with Oh-My-Fish.

### Bug Cause:
The bug is caused by the incomplete parsing of the output obtained from the subprocess. The function is not correctly extracting only the version number from the shell's response.

### Fix Strategy:
To fix the bug, the function needs to correctly extract the version number from the response obtained by running the subprocess command.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(', version ')[1]  # Extracting the version number
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output based on the string ', version ', we can effectively get the actual version number. This updated version should correctly extract the version without any additional text, resolving the bug and passing the failing test.