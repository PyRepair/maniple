### Analysis
The issue at hand is due to the fact that the function `info()` is returning the entire output of the command `echo $FISH_VERSION`, which includes the text 'fish, version'. This is causing the assert statement in the test to fail, as it is expecting only the version number.

### Bug Location
The bug is located in the line where `version = proc.stdout.read().decode('utf-8').strip()` is executed. This line reads the entire output of the command without extracting just the version number.

### Cause of the Bug
The cause of the bug is that the function is not parsing the output of the command correctly. It is returning the entire output string, including 'fish, version', whereas it should only return the version number. This mismatch in the expected and actual output is causing the test to fail.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the line that extracts the version number from the command output. We should only extract the version number and discard the rest of the output to match the expected output in the test.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output of the command and extracting the last element (which is the version number), we ensure that the function only returns the version number without any additional text. This corrected version should pass the failing test and match the expected output.