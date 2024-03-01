### Analysis
1. The `info()` function is supposed to extract the version number from the `fish` shell and return it in a specific format. The failing test indicates that the expected output is `'Fish Shell 3.5.9'` while the actual output includes extra characters (`'fish, version'`).
2. The issue lies in the line where the version is extracted (`version = proc.stdout.read().decode('utf-8').strip()`). It is reading the output as-is without correctly separating the version number.
3. The runtime input shows that the extracted version is `'fish, version 3.5.9'` instead of just `'3.5.9'` as expected.
4. To fix this bug, we need to split the extracted output to only include the version number without the unnecessary characters.
5. Below is the corrected version of the `info()` function.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1] # Extract only the version number
        return u'Fish Shell {}'.format(version)
``` 

By splitting the extracted output to only include the version number, the corrected function will return `'Fish Shell 3.5.9'` as expected.