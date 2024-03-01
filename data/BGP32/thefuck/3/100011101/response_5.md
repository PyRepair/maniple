### Explanation:
The bug in the provided function is caused by the fact that the `info` function is returning the entire string `'fish, version 3.5.9'` instead of just the version number `'3.5.9'`. This is evident from the failing test where the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.

The issue arises because the function is not correctly extracting just the version number from the output of the shell command. 

### Strategy for fixing the bug:
To fix the bug, we need to modify the code to extract only the version number from the output of the shell command, instead of returning the entire string. 

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip()  # Extracting just the version number
    return u'Fish Shell {}'.format(version)
``` 

With this corrected version, the function should now correctly extract the version number and return the expected output `'Fish Shell 3.5.9'`.