### Analyze
- The buggy function `info` is a method of the class `Fish`.
- The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
- The function is supposed to retrieve the version of the Fish shell from the environment variable `$FISH_VERSION`.
- The GitHub issue suggests that the shell command `thefuck -v` triggers a hang due to a recursive loop caused by the `info` function.

### Potential Error Locations
1. The handling of the output from Popen might not be correct.
2. The parsing of the version number from the command output could be incorrect.

### Bug Cause
The bug is caused by the incorrect parsing of the version number from the output of the shell command. The function is assuming that the output contains only the version number when in fact it includes additional text.

### Bug Fix Strategy
To fix the bug, we need to modify the way we extract the version number from the command output. We should ensure that only the version number is included in the final output string.

### Corrected Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        
        # Extract the version number from the output
        version = output.split(' ')[-1]
        
        return u'Fish Shell {}'.format(version)
```

By splitting the output using a space and taking the last element, we ensure that only the version number is extracted. This should resolve the bug and produce the expected output.