### Analysis
- The error message highlights the assertion failure, indicating that the expected output 'Fish Shell 3.5.9' does not match the actual output 'Fish Shell fish, version 3.5.9'.
- The runtime values show that the `version` variable contains the output 'fish, version 3.5.9' instead of just the version number.
- The issue seems to be with how the version information is extracted from the command output.

### Bug
The bug in the function lies in the way the version information is retrieved from the command output. The `version` variable includes unnecessary text 'fish, version' along with the version number, leading to a mismatch in the expected and actual outputs.

### Fix Strategy
To fix the bug, we need to extract only the version number from the command output and format it correctly to match the expected output.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_number = version.split(',')[1].strip()
        return u'Fish Shell {}'.format(version_number)
``` 

By splitting the `version` string at the comma and selecting the second part, we extract only the version number before formatting it as expected. This corrected version should resolve the bug and pass the failing test.