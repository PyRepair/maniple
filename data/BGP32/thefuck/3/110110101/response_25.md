## Analysis
The buggy function `info` in the Fish shell class is supposed to return the name and version of the current shell by executing a command in the shell. The bug seems to be related to how the version information is extracted from the command output.

The failing test provides the expected output as `'Fish Shell 3.5.9'`, but the actual output includes unwanted characters `'fish, version '`. This indicates that the parsing of the version number from the command output is incorrect.

## Bug
The bug lies in how the version information is processed from the output of the command `echo $FISH_VERSION`. The current implementation does not accurately extract only the version number and includes unwanted characters.

## Fix
To fix the bug, we need to correctly parse and extract only the version number from the command output. We can achieve this by removing the unwanted characters 'fish, version ' and only keeping the version number '3.5.9'.

Here is the corrected version of the function:

```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will return the expected version number by eliminating the unwanted characters. This should make the function pass the failing test.