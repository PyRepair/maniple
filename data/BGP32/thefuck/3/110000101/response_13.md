### Analysis
- The `info` function is supposed to retrieve the version of the Fish shell by running a command in the terminal.
- The issue seems to be related to how the output of the `Popen` process is being handled. The code attempts to read the output directly from `proc.stdout`, but it is not done correctly.
- The `proc.stdout.read()` call returns a byte-based string that needs to be decoded before being converted to a regular string.

### Bug Explanation
- The bug arises because the output of `proc.stdout.read()` is not properly decoded before trying to convert it to a string. This results in an incorrect value for the `version` variable.

### Fix Strategy
- Decode the byte-based output of `proc.stdout.read()` using the correct encoding before converting it to a regular string.

### Corrected Code
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```