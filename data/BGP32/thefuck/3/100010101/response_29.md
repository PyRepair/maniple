### Analysis
- The `info` function is meant to return the name and version of the current shell by running a command using `Popen`.
- The error message indicates that the function is not correctly parsing the version number from the output of the `Popen` command.
- The expected version number is `'3.5.9'` but the function is returning `'fish, version 3.5.9'`.
- This suggests that the string `'fish, version '` is unintentionally included in the output.

### Bug
The bug is caused by the fact that the function is not correctly stripping the extra characters from the version output obtained from the `Popen` command.

### Fix
To fix this bug, we need to modify the function to extract only the version number from the output and remove any unwanted characters.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()  # Read the output
    version = version_output.split(', version ')[1]  # Extract the version number
    return u'Fish Shell {}'.format(version)
``` 

This corrected version extracts the version number by splitting the output around `', version '` and taking the second part. This ensures that only the raw version number is returned.