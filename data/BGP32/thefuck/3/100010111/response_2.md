### Analysis
1. The buggy function `info` is supposed to return the name and version of the current shell, but it is not retrieving the correct version.
2. The expected version '3.5.9' is not being extracted properly from the Popen process output.
3. The error message shows that the retrieved version includes extra text 'fish, version' which is not expected.
   
### Bug Explanation
The cause of the bug lies in the way the version is extracted from the Popen process output. Instead of extracting only the version number, the current implementation includes the extra string 'fish, version' as well. This results in a mismatch with the expected value, leading to a failing test.

### Strategy for Fixing the Bug
To fix this bug, the extraction of the version number from the Popen process output needs to be corrected. The function should only return the version number without any extra strings like 'fish, version'.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[0].split()[-1]  # Extract just the version number
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the extracted version will only contain the version number itself, resolving the issue.