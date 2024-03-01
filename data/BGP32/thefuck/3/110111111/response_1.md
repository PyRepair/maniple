## Bug Analysis
1. The buggy function `info` in the `Fish` class is supposed to return the name and version of the current shell by executing a command to retrieve the Fish shell version.
2. The failing test provides a hardcoded version output that the function should match.
3. The error occurs because the function incorrectly returns the entire output from the command execution, including the text "fish, version" which is not part of the version number.
4. The expected version value is `'3.5.9'` based on the failing test.

## Bug Fix Strategy
To fix the bug, we need to modify the method to extract just the version number from the output of the executed command.

## Updated Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extracting only the version number
        version_number = version.split(' ')[-1]
        return u'Fish Shell {}'.format(version_number)
```

By splitting the output of the `fish -c 'echo $FISH_VERSION'` command and extracting the last part as the version number, we ensure that only the actual version number is used for the return value. This corrected version should now pass the failing test and match the expected output `'Fish Shell 3.5.9'`.