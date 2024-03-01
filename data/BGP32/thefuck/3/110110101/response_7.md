### Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell and return it in a specific format. The failing test provides the version in the format `'Fish Shell 3.5.9'`, but the function currently extracts the version as `'3.5.9'` without adding the preceding text.

### Bug
The bug is in the return statement of the `info` function. It is missing the prefix `'Fish Shell '` before the version.

### Fix
To fix the bug, we need to modify the return statement to include the prefix `'Fish Shell '` before the extracted version.

### Corrected Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```