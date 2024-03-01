### Identified Bug:
The bug in the `info` function is that the version string retrieved from the `fish` command includes extra information that is not part of the version number. This extra information causes the assertion in the test to fail since the expected version number does not match the actual version number extracted from the output.

### Cause of the Bug:
The `info` function extracts the version information using the command `fish -c 'echo $FISH_VERSION'`. This command returns the version along with additional text that includes "fish, version" before the actual version number. The function then attempts to format this information into the expected output, resulting in a mismatch.

### Strategy for Fixing the Bug:
To fix the bug, the function needs to extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. This can be achieved by parsing the output to extract just the version number without any additional text.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_detail = proc.stdout.read().decode('utf-8').strip()
    version = version_detail.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function should now correctly extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command, leading to a successful test execution and resolving the reported issue in the GitHub repository.