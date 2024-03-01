### Analysis
1. The buggy function `info` in the `Fish` class is trying to retrieve the Fish shell version by running a command `echo $FISH_VERSION` using the `Popen` function.
2. The failing test `test_info` sets up the `Popen` mock to return a string containing the version number `3.5.9`, but the returned value from the `info` function includes the string `'fish, version'` before the actual version number.
3. The error message shows that the expected output is `'Fish Shell 3.5.9'` but the actual output includes `'fish, version 3.5.9'`.
4. The bug is in the line where the version is being extracted from the command output.
5. We need to modify the code to correctly parse the version number from the output of the command.

### Bug Fix Strategy
1. Modify the code to properly extract only the version number from the output of the command.
2. Update the code to handle the command output format correctly to obtain the desired version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        
        # Extracting the version number only
        version = version_output.split(', version ')[1].strip()
        
        return u'Fish Shell {}'.format(version)
```

After applying this fix, the corrected function should correctly extract the version number and provide the expected output `'Fish Shell 3.5.9'` as required by the failing test.