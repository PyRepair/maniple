### Analysis
The bug in the function lies in extracting the version number from the output of the `echo $FISH_VERSION` command. In the buggy implementation, the entire output string `'fish, version 3.5.9'` is being used as the version, instead of extracting just the version number `3.5.9`.

### Bug Fix Strategy
1. Parse the output string to extract only the version number.
2. Update the return statement to use the extracted version number to correctly format the shell name.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output string `'fish, version 3.5.9'` using `, version ` as the delimiter and extracting the second part, we can correctly obtain the version number `3.5.9` as expected. This corrected version of the function should now pass the failing test.