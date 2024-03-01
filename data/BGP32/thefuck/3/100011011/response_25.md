### Bug Analysis:
The buggy function `info` is attempting to retrieve the version of the Fish Shell by executing a command and reading the output. However, the function is not correctly parsing the version information. This results in the output containing additional information such as "fish, version" which causes the comparison in the test to fail.

The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output contains additional text `'fish, version 3.5.9'`.

### Bug Location:
The issue lies in how the version information is extracted from the output of the command.

### Bug Cause:
The command `echo $FISH_VERSION` returns the output with the text 'fish, version' included in it. This causes the additional text to be present in the version string read by the function. As a result, the comparison in the test fails.

### Proposed Fix:
To fix the bug, we need to modify the way the version information is extracted from the output. We should remove the unnecessary text and only keep the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number from the output
    version = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By splitting the version information based on the comma and keeping only the second part (which contains the version number), we can ensure that the function returns only the version number without any additional text. This should resolve the issue and make the test pass.