### Analysis
The buggy function is trying to retrieve the Fish shell version by running the command `echo $FISH_VERSION` using `Popen`. The issue is with the format of the version string being retrieved, which includes extra text like "fish, version".

### Bug
The bug in the function is caused by not extracting only the version number from the output of the command `echo $FISH_VERSION`. The extracted version string contains additional text like "fish, version".

### Fix
To fix the bug, we need to modify the code to extract only the version number from the output of the command.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
``` 

This corrected version of the function will strip the output and extract only the version number, fixing the bug.