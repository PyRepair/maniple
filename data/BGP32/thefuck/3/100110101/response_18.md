### Analysis
- The `info` function is trying to get the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and extracting the version number from the output.
- The failing test is setting the return value of `stdout.read` to `b'fish, version 3.5.9\n'`, which is causing the discrepancy in the version number comparison. 
- The expected output is `'Fish Shell 3.5.9'` but the buggy function is including the extra text `'fish, version'` in the version string.

### Bug Cause
The bug is caused by not properly parsing the version number extracted from the command output. The function is not correctly handling the formatting of the output.

### Strategy for fixing the bug
To fix the bug, we need to properly parse the version number from the output of the command and format it correctly in the return statement. We should remove any additional text before or after the version number to ensure the output matches the expected value.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()  # Extract only the version number from the output
    return u'Fish Shell {}'.format(version)
``` 

After making the above correction, the function should be able to correctly extract and format the version number from the command output, fixing the bug and passing the failing test.