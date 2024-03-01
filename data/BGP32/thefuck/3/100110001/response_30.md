### Analysis:
1. The buggy function `info` in the `fish.py` file is attempting to get the version of the Fish shell by executing a command and capturing the output, but it is not correctly targeting the version output.
2. The failing test `test_info` is setting up a mock behavior for the `Popen` call to return the version string in the expected format.
3. The error message indicates that the actual output of the `info` function includes additional text (`fish, version`) that is not expected.
4. The bug is caused by capturing the entire output of the command instead of just the version number itself.
5. To fix the bug, we need to modify the way the output is captured from the `Popen` call.

### Strategy for Fixing the Bug:
1. Modify the way the output is captured from the `Popen` call to only extract the version number.
2. Update the decoding of the output to correctly strip any unwanted characters.
3. Adjust the string formatting to include the extracted version number.

### Corrected Version of the Function:
```python
from typing import List

def info(self):
    """Returns the name and version of the current shell"""
    version = self._get_fish_version()
    return f'Fish Shell {version}'

def _get_fish_version(self) -> str:
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
    return version
``` 

In the corrected version:
- The `_get_fish_version` method is introduced to correctly extract and return the version number.
- The `info` method now calls the `_get_fish_version` to retrieve the version and formats the output string accordingly. 

This corrected version should pass the failing test.