### Analysis
1. The function `info` in the `Fish` class is supposed to return the name and version of the current shell by running a command to get the version from the Fish shell.
2. The error occurs because the expected output of the function is not matching the actual output. The version extracted from the command includes the text "fish, version" along with the version number, leading to the mismatch in the assertion.
3. The bug is caused by not properly parsing the output of the command to extract only the version number without the additional text.
4. The fix involves modifying the way the version number is extracted from the command output.
5. Below is the corrected version of the `info` function:

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        
        # Extract only the version number from the command output
        version_start = version_output.find('version') + len('version') + 1
        version = version_output[version_start:]
        
        return u'Fish Shell {}'.format(version)
```