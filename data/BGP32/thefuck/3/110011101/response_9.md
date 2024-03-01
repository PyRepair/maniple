### Analysis
- The buggy function `info` is currently retrieving the version information for Fish shell using a command that returns the version with additional text (`'fish, version'`).
- The test is failing because the expected output does not match the actual output due to the additional text `'fish, version'` present in the version string.
- The `assert` statement is comparing the full output string instead of just the version number.
- The `version` variable is not being correctly extracted from the output.
- The function should extract only the version number without the `'fish, version'` prefix.

### Bug Fix Strategy
1. Modify the extraction of the version to remove the `'fish, version'` prefix.
2. Update the `assert` statement to only compare the extracted version number with the expected version.
3. Ensure that the return statement formats the version number correctly with the prefix `'Fish Shell'`.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(' ')[-1]  # Extract only the version number by removing the prefix
        return u'Fish Shell {}'.format(version)
```

By modifying the version extraction logic and the format of the return statement, the corrected function should now correctly extract and display only the version number without any additional text. This change should make the function pass the failing test and return the expected output `'Fish Shell 3.5.9'` as desired.