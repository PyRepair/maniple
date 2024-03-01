### Analysis
The buggy function `info` is supposed to return the name and version of the current shell. However, the issue lies in how it retrieves the version from the `stdout` of the `Popen` process. The current implementation does not correctly handle the output. The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes the unwanted `'fish, version '`. This leads to the assertion error.

### Error Cause
The cause of the bug is that the original implementation of the `info` function does not correctly extract only the version number from the output of the `Popen` process, causing the version string to include unwanted characters.

### Fix Strategy
To fix this bug, we need to modify the `info` function to extract the version number correctly. We should only extract the version number itself without any extra characters to match the expected output.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip() 
    version = version.split(",")[1].strip()  # Extract only the version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the version string and extracting the version number properly, we ensure that only the version number is returned without any additional characters. This correction should address the bug and make the function return the expected output.