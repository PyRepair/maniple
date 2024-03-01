## Analysis
1. The error message is showing that the expected output is `'Fish Shell 3.5.9'` and the actual output is `'Fish Shell fish, version 3.5.9'`.
2. The buggy function `info` is using the shell command `echo $FISH_VERSION` to retrieve the version number of the Fish Shell. However, the command is returning `fish, version 3.5.9` instead of just the version number.
3. The bug is caused by the fact that the output of the command includes additional text that is not needed when extracting the version number. This causes the comparison to fail.
4. A strategy to fix this bug is to modify the `info` function to properly extract and format the version number from the command output.

## Fixing the Bug

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        # Extract the version number from the output
        version = version_output.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

By splitting the version output using `,` and taking the second part after the split, we can extract only the version number without any additional text. This will ensure that the function returns the correct version output that can be compared successfully in the test.