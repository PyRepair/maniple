### Analysis
1. The function `info` in the `Fish` class is attempting to retrieve the version of the Fish shell by executing a command in a subprocess.
2. The error message is indicating that the expected output is slightly different from the actual output. The version is being extracted correctly, but the formatting of the output string is incorrect.
3. The bug is caused by the formatting string not correctly incorporating the version number of the Fish shell.
4. To fix the bug, we need to update the formatting string to include the version extracted from the subprocess correctly.
5. Below is the corrected version of the function:

### Corrected Version
```python
# The corrected version of the function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By correcting the formatting string in the return statement as shown above, the function now correctly returns the expected output `'Fish Shell 3.5.9'`.