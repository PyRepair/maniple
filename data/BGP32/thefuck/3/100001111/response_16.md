The buggy function `info` is attempting to retrieve the version of Fish Shell by running the command `fish -c 'echo $FISH_VERSION'`. The issue lies in the fact that the command is returning the full version with extra text, not just the version number, causing the function to output incorrect information.

To fix this bug, we need to extract only the version number from the output of the command and return it. We can do this by splitting the output string and extracting the version number part.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
``` 

This corrected version should now properly extract the version number and output it correctly as expected by the failing test cases.