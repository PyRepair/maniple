### Analysis
- **Buggy Function**: The `info` function in the `Fish` class is intended to return the name and version of the Fish shell.
- **Test Code**: The failing test for the `info` function of the `Fish` class sets up a mock process to simulate the output of the `fish, version 3.5.9` command.
- **Error Message**: The assertion error occurs because the expected output is `'Fish Shell 3.5.9'` but the function returns `'Fish Shell fish, version 3.5.9'`.
- **Runtime Input/Output**:
  - The `proc.stdout.read()` call in the function returns `'fish, version 3.5.9'`.
  - The function returns `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
- **Expected Input/Output**:
  - The function should extract only the version number from the output and return `'Fish Shell 3.5.9'`.
- **GitHub Issue**: The issue is related to a recursive loop triggered by using `thefuck -v` with the Oh-My-Fish plugin.

### Bug Cause
The bug is caused by the function not correctly extracting only the version number from the output of the subprocess command, leading to the incorrect formatting of the returned string.

### Fix Strategy
To fix the bug, we need to modify the function to extract only the version number from the output of the subprocess command and format it correctly.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[1].strip().replace('version', '')
        return u'Fish Shell {}'.format(version)
```

With this correction, the `info` function in the `Fish` class should now correctly extract only the version number from the output and return the formatted string `'Fish Shell 3.5.9'`.