### Potential Error Location
The error in the function is likely related to how the version information is being extracted from the output of the `fish -c 'echo $FISH_VERSION'` command.

### Cause of the Bug
The bug is caused by the fact that the output of the `fish -c 'echo $FISH_VERSION'` command includes the text `'fish, version 3.5.9'`, which is not the correct format for extracting the version number directly.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the parsing of the version information to extract only the version number without any additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

This corrected version reads the output of the command, splits it by `,`, and takes the second part which contains the version number. It then formats this version number with the shell name and returns the correct output.