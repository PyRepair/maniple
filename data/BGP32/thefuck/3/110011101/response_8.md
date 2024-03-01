### Analysis
1. The buggy function is attempting to extract the version of the Fish shell by running a command in a subprocess. It then reads the output to get the version.
2. The error occurs because the `version` variable includes additional text ("fish, version") that needs to be stripped before constructing the return string.
3. At runtime, the function retrieves the version information but includes the unnecessary text prefix "fish, version".
4. To fix the bug, we need to strip the unwanted text from the version before constructing the return string.
5. The corrected version of the function:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]  # Extract the version only
        return 'Fish Shell {}'.format(version)
``` 

By splitting on the ", " delimiter and taking the second part (index 1) of the resulting list, we eliminate the unwanted text and only return the version number in the expected format.