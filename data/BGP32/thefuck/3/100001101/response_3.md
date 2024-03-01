### Analysis
The buggy function is trying to get the version of the current Fish shell by running a command and capturing the output. The issue seems to be with how the version is extracted from the output of the command.

### Bug
The bug appears to be in how the function is extracting the version from the output of the command. It currently includes "fish, version" in the version string, which is unnecessary. The expected version does not have this prefix.

### Fix Strategy
To fix the bug, we need to modify the code to extract only the version number without any additional prefixes.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(",")[1].strip()
    return u'Fish Shell {}'.format(version)
```