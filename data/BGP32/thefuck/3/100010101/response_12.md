### Analysis
- The buggy function `info` is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` and returning it with a formatted string.
- The error message indicates that the returned value includes the text "fish, version", which is unexpected.
- The Popen process is mocked in the test with the expected output value of `'fish, version 3.5.9\n'`.
- The bug seems to be related to how the version is extracted from the command output in the function.

### Bug Cause
- The bug is caused by directly reading the output of `proc.stdout` without considering the complete output format returned from the command.
- The function is reading the entire output, including unwanted text like "fish, version".

### Fix Strategy
- Modify the way the version is extracted from the command output to only include the version number.
- Update the decoding and stripping process to obtain only the version number without the extra text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output on spaces and getting the last element from the split result, we ensure that we only extract the version number without any unwanted text.