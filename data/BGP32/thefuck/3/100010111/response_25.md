### Analysis:
The current buggy function attempts to retrieve the version of the Fish Shell by executing a command using a Popen subprocess. However, the version retrieved includes more text than just the version number, hence causing the assertion error in the test case. The function is not properly extracting the version number from the command output.

### Error Cause:
The cause of the bug is the incorrect handling of the output from the Popen subprocess. The expected version number is '3.5.9', but the current implementation also includes extra text 'fish, version' in the output. This discrepancy causes the assertion error.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the way we extract the version number from the command output. We should extract only the version number portion of the output and exclude any other accompanying text.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
    return u'Fish Shell {}'.format(version)
```

The corrected version of the function splits the output by `,` and takes the second part, which should contain just the version number '3.5.9'. This modification ensures that only the version number is included in the final string without any extra text.