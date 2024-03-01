### Analysis
1. **Buggy Function and Class Relationship**: The buggy function `info` is a method within the `Fish` class.
2. **Error Message**: The `assert shell.info() == 'Fish Shell 3.5.9'` failed because the actual output was `'Fish Shell fish, version 3.5.9'`.
3. **Expected Input/Output**:
    - Input: No direct input mentioned, but the function fetches the version of the Fish Shell.
    - Output:
        - Before fix: `'Fish Shell fish, version 3.5.9'`
        - After fix: `'Fish Shell 3.5.9'`
4. **GitHub Issue**: The issue states that the usage of the `-v` flag in the Oh-My-Fish plugin triggers a recursive loop due to the `info` method in `shells/fish.py`.

### Bug Location
The issue is likely with how the output is being processed after executing the command to get the Fish Shell version. The current version string includes extra characters `'fish,'` which causes the test to fail.

### Bug Cause
The `FISH_VERSION` variable includes the text `'fish, version'` before the actual version number which results in the incorrect output of `'Fish Shell fish, version 3.5.9'`.

### Fix Strategy
We need to strip the unwanted text from the version string to get only the version number before formatting it into the desired output format.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Remove unwanted text before the version number
        version = version.split(' ')[-1]
        return f'Fish Shell {version}'
``` 

By splitting the version string based on spaces and taking the last element, we ensure that only the actual version number is used in the output. This corrected version should resolve the issue and produce the expected output.