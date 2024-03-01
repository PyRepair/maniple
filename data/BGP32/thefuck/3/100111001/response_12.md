### Analysis:
1. The `info` function in the `Fish` class is intended to retrieve the version of the Fish shell by executing a command and extracting the version information.
2. The test function `test_info` is mocking the `Popen` object and setting up a side effect to return the version information.
3. The error occurs because the expected output `'Fish Shell 3.5.9'` does not match the actual output `'Fish Shell fish, version 3.5.9'`.
4. The discrepancy in the output indicates that the version string is being retrieved incorrectly from the command output.

### Bug:
The bug lies in how the version information is extracted from the command output. The function is not parsing the correct part of the output to get only the version number.

### Fix:
Modify the function to correctly extract the version number from the output of the `echo $FISH_VERSION` command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will extract only the version number from the output and return it in the format `'Fish Shell <version>'`.