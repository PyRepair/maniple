Based on the provided information, the bug in the `info` function of the `Fish` class arises from how the version of Fish shell is obtained and formatted. The version extracted from the command output includes unnecessary text that causes the assertion failure in the test.

### Bug Explanation:
The function retrieves the version as `'fish, version 3.5.9'`. However, the expected version should be simply `3.5.9`. This discrepancy in the version leads to the assertion failure because the returned value includes the extra text `'fish, version '`.

### Fix Strategy:
To fix the bug, the function needs to extract only the version number from the output and format the return value as `'Fish Shell {}'`. This will ensure the version is correctly parsed and formatted without unnecessary text.

### Corrected Version of the Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By modifying the function to extract only the version number from the output, the corrected version should now return `'Fish Shell 3.5.9'` as expected and resolve the issue reported on GitHub related to oh-my-fish/plugin-thefuck#11.