The bug in the provided function arises from not extracting the version number correctly from the output of the command 'echo $FISH_VERSION'. 

- The runtime values show that the `version` variable contains the string `'fish, version 3.5.9'`, which is not the expected format.
- The expected values indicate that the `version` variable should only contain the version number `'3.5.9'`.

To fix this bug, we need to modify the code to extract only the version number from the output. We can do this by splitting the output string and taking the last part of it, assuming that the version number is always the last part of the output.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

With this modification, the function should now correctly extract and return the version number as expected.