### Analysis
The error message indicates that the `shell.info()` function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`, which causes the assertion to fail. This discrepancy is likely due to how the function is extracting the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.

### Error locations
1. The function is extracting the version number from the output incorrectly.
2. The formatting of the output string `'Fish Shell {}'` is not correctly incorporating the version number.

### Bug Cause
The bug in the code is caused by the incorrect extraction of the version number from the shell command output. Since the version number is preceeded by `'fish, version'`, the `decode`, `strip`, and concatenation operations need to be adjusted to correctly extract and format the version number.

### Fix Strategy
1. Update the decoding, stripping, and formatting process to correctly extract the version number from the command output.
2. Ensure that the formatted output string includes the extracted version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]  # Extracting version number correctly
    return u'Fish Shell {}'.format(version)
``` 

With this corrected version of the function, it should correctly extract the version number from the output of the `fish -c 'echo $FISH_VERSION'` command and return `'Fish Shell 3.5.9'`. This will resolve the assertion error and address the issue reported on GitHub.