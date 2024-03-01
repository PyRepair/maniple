### Analysis
- The buggy function is attempting to retrieve the version of the Fish shell using a subprocess call to `fish -c 'echo $FISH_VERSION'`.
- The issue seems to stem from the returned version including extra text ("fish, version").
- The error message shows that the expected version is "3.5.9" but the actual value includes the unnecessary text ("fish, version").
- The `decode('utf-8')` operation on `proc.stdout.read()` seems to be the cause of the issue.

### Fix Strategy
To fix the bug, we need to strip the additional text ("fish, version") from the output returned by the subprocess call. This can be achieved by modifying the way the output is processed before returning the version.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extracting the version part
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output based on whitespace and taking the last element, we ensure that only the version number is considered, addressing the issue of the unnecessary text.