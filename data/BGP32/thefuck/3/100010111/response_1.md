## Analysis
1. The buggy function `info` is using `Popen` to execute a command in the Fish shell and retrieve the version number. It then formats this version number into a string with the prefix `"Fish Shell "`.
2. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes the string `'fish, version 3.5.9'`, leading to an assertion error.
3. The cause of the bug is that the command `echo $FISH_VERSION` is returning the version number with additional text that is not handled correctly by the function.
4. To fix the bug, we need to modify the function to extract only the version number from the output of the shell command.
5. We need to modify the function to correctly extract and format the version number.

## Updated Function
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

This updated function will correctly extract the version number from the output of the `echo $FISH_VERSION` command and format it as `'Fish Shell 3.5.9'`.