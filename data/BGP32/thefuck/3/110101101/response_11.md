## Bug Explanation
The bug in the `info` function is that it is expecting the output of the `fish -c 'echo $FISH_VERSION'` command to include the string `'fish, version'` in order to extract the version number. However, the actual output of the command is `'fish, version 3.5.9\n'`, which does not match the expected format.

## Fix Strategy
To fix this bug, we need to modify the way we extract the version number from the output of the command. We should split the output by space and take the last element of the resulting list as the version number.

## The Corrected Version
```python
# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
        return u'Fish Shell {}'.format(version)
```