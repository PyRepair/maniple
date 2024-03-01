### Potential Error Locations:
1. The command used in Popen to get the Fish shell version might not be correct.
2. The decoding of the stdout might be causing issues with extracting the version string.
3. The format string used to return the shell information might not be correctly configured.

### Cause of the Bug:
The buggy function `info` is using the command `fish -c 'echo $FISH_VERSION'` to retrieve the Fish shell version. However, the test is expecting the command to be `fish --version` which is causing a mismatch in the extracted version string. Additionally, the function is not correctly handling the output decoding, leading to the inclusion of unnecessary text in the version string.

### Strategy for Fixing the Bug:
1. Change the command in Popen to `['fish', '--version']` to match the test expectations.
2. Modify the decoding process to correctly extract only the version number.
3. Update the format string to properly display the shell information.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

By making these changes, the function should now accurately extract the Fish shell version in the expected format, passing the failing test and resolving the GitHub issue.