### Analysis
1. The `info` function in the `Fish` class is attempting to retrieve the version of the Fish shell by executing a command. The version is then extracted from the output of the command and returned as a formatted string.
2. The error message indicates that the function is not returning the expected version of the Fish shell.
3. The cause of the bug is that the function is not correctly handling the output of the executed command. The output contains additional text "fish, version" which is not expected in the version number.
4. To fix the bug, we need to modify the extraction of the version from the command output to only include the version number.
5. A corrected version of the function is provided below.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.split(',')[1].strip()  # Extract only the version number
        return 'Fish Shell {}'.format(version)
```

With this corrected version, the function will properly extract the version number from the command output and return it formatted as "Fish Shell {version}". This will satisfy the expected output value and pass the failing test.