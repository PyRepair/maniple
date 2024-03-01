### Bug Analysis:
1. **Buggy Function and Class Relationship**: The `info` function is part of the `Fish` class, which is a subclass of `Generic`.
   
2. **Error Message**: The assertion error occurs when comparing the expected output `'Fish Shell 3.5.9'` with the actual output `'Fish Shell fish, version 3.5.9'`.
   
3. **Runtime Input/Output Values**:
   - `version`: `'fish, version 3.5.9'`
   
   The function is returning the version string without stripping the unwanted characters, leading to the incorrect output.
   
4. **Expected Input/Output Values**:
   - `version`: `'3.5.9'`
   
   The correct output should be `'Fish Shell 3.5.9'`.
   
5. **GitHub Issue**: The issue is related to using `thefuck -v` with Fish Shell causing a recursive loop, which is partially connected to the buggy function `info`.

### Bug Fix Strategy:
The bug is caused by not stripping the unwanted characters from the version string. To fix the bug, modify the function to extract only the version number from the provided string.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By splitting the version string and retrieving only the version number part, the corrected function will return `'Fish Shell 3.5.9'` as expected, resolving the assertion error.