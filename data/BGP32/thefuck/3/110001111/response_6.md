### Analysis
1. The buggy function `info` in class `Fish` is attempting to retrieve the version of the Fish shell and construct a message with that version.
2. The function uses `Popen` to execute a command `echo $FISH_VERSION` in the Fish shell, but it seems to be incorrectly parsing the output.
3. The expected output should be just the version number without any additional text.
4. The issue on GitHub indicates that this buggy behavior is causing a recursive loop, which needs to be fixed promptly.

### Bug Explanation
The bug is caused by the function not correctly stripping the output of the command `echo $FISH_VERSION`, which results in additional text being included in the version variable.

### Bug Fix Strategy
To fix the bug, we need to ensure that only the version number is extracted from the output of the command and stored in the `version` variable.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Get the last part as the version
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output and taking the last part as the version, we ensure that only the version number is used in the constructed message. This corrected version should resolve the bug and prevent the recursive loop mentioned in the GitHub issue.