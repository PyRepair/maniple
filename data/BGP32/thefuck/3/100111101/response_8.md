### Analysis
The buggy function is trying to get the version of the Fish shell by running a command and capturing the output. The issue lies in the command being executed (`echo $FISH_VERSION`) and the way the version is extracted from the output. The failing test is due to the incorrect comparison of the expected version string ('Fish Shell 3.5.9') with the actual output ('Fish Shell fish, version 3.5.9').

### Bug
The bug arises because the command executed in the `Popen` call is incorrect and the extraction of the version from the output is not handling the output format properly.

### Fix
To fix the bug, the command executed should be changed to `fish --version` to get the correct version output and then extract the version number. Additionally, we need to modify the extraction logic to remove unnecessary text from the output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split(", ")[1]
    return u'Fish Shell {}'.format(version)
```