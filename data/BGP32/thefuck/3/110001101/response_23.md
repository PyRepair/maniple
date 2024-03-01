### Explanation:
The bug in the provided function is caused by not properly handling the output of the `Popen` process. The function is expecting the version string to be returned directly from the command `echo $FISH_VERSION`, but it is actually returning `'Fish Shell version 3.5.9'`. This causes the function to include extra text in the output.

### Strategy for fixing the bug:
1. Modify the command passed to `Popen` to only extract the version number without additional text.
2. Update the parsing of the output to extract the version number correctly.

### Corrected version of the function:
```python
# The corrected version of the buggy function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[2]  # Extracting only the version number
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output and extracting the version number specifically, the corrected function will return the expected version string `'Fish Shell 3.5.9'`.