### Analysis
1. The buggy function `info` is attempting to retrieve the version of the Fish shell by executing a command and capturing its output. However, the current implementation includes the word "fish, version" as part of the captured version, leading to a mismatch during the comparison with the expected output.
2. The issue lies in the way the version string is extracted and formatted from the command output.
3. In the failing test, the command output includes the string "fish, version 3.5.9" which is not expected. The function should only return the version number itself without any additional text.
4. To fix the bug, we need to modify the way the version string is extracted and formatted in the function.

### Bug Fix
Here is the corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the version string based on ", version ", we can extract just the version number without any additional text. This correction should now match the expected output and pass the failing test.