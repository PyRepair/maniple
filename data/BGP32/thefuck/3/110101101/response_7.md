### Analysis
The buggy function `info` is supposed to get the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and extracting the version number from the output. However, in the failing test, the expected version number is `'3.5.9'`, but the actual version number extracted from the command output is `'fish, version 3.5.9'`. This discrepancy is causing the test to fail.

### Bug Identification
The bug is in the way the version number is extracted from the command output. The function is currently using the entire output string without filtering out the unnecessary prefix `'fish, version '`.

### Bug Explanation
The bug is causing the extracted version number to include unwanted text, specifically the `'fish, version '` prefix. This incorrect version number then fails the equality check in the test.

### Bug Fix
To fix the bug, we need to modify the way the version number is extracted to remove the unwanted text prefix. We can achieve this by splitting the output string and only taking the version number part.

### The corrected version of the function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output string using `', version '` and taking the second element from the resulting list, we extract only the version number without the unwanted prefix. This corrected version of the function should now pass the failing test and return the expected version number `'3.5.9'`.