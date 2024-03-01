### Bug Explanation
The buggy function `info` is trying to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using subprocess `Popen`. However, it is expecting the output to be only the version number (`3.5.9`), but the actual output includes additional text (`fish, version 3.5.9`), causing the assertion error in the test.

### Bug Fix
To fix the bug, we need to update the command that is being executed to retrieve only the version number without any extra text. We can modify the command to `fish --version` which will provide the output in the desired format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    _, version_text = version.split(', version ')
    return u'Fish Shell {}'.format(version_text)
``` 

By updating the command to `fish --version` and extracting only the version number part from the output, we ensure that the function correctly returns the desired output and passes the test.