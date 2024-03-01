### Analysis
The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell. The issue lies in the command used to retrieve the version, which is incorrect. The test is expecting the version number to be '3.5.9' but the function is returning 'fish, version 3.5.9'. This mismatch causes the test to fail.

### Bug Explanation
The function is using the command `echo $FISH_VERSION` to retrieve the version number. However, this command outputs 'fish, version 3.5.9' instead of just the version number '3.5.9'. This string mismatch between the expected and actual output causes the assertion to fail.

### Bug Fix
To fix this bug, we need to modify the command used to extract the version number in the `info` function. We should update the command to just output the version number without any additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'fish --version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extracting the version number only
    return u'Fish Shell {}'.format(version)
``` 

By updating the command to retrieve the version number correctly and extracting only the version number from the output, the corrected function should now return 'Fish Shell 3.5.9' as expected.