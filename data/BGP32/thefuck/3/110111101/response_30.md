### Bug Analysis
The bug in the `info` function lies in the way it retrieves the version information of the Fish shell. The function expects the output of the `fish -c 'echo $FISH_VERSION'` command to be only the version number, but the actual output includes extra text.

The failing test provides the output `'fish, version 3.5.9'`, while the function is expecting just `'3.5.9'`. This mismatch causes the assertion failure.

### Bug Fix Strategy
To fix the bug, we need to modify the parsing of the version information to extract only the version number without any extra text.

### Corrected Code
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        raw_version = proc.stdout.read().decode('utf-8').strip()
        version = raw_version.split()[-1]
        return u'Fish Shell {}'.format(version)
```

With this corrected code, we extract the last word from the string obtained from the command output, which represents the version number. This modification ensures that only the version number is included in the return value of the function, matching the expected output of the failing test.