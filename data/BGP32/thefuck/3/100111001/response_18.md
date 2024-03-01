### Analysis:
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish Shell by running the command `echo $FISH_VERSION` in a subprocess.
2. The failing test sets up the mock behavior to return `b'fish, version 3.5.9\n'` when `Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)` is called.
3. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
4. The bug seems to be related to the way the output of the subprocess command is being processed and formatted to get the version information.

### Bug:
The bug lies in the way the version output from the subprocess is being extracted and formatted. The current implementation does not handle the output from the `echo $FISH_VERSION` command correctly, resulting in the additional `fish,` prefix in the version string.

### Fix:
To fix the bug, we need to modify the way we extract and format the version output from the subprocess. We should split the version string based on the `,` delimiter and extract the version number after 'version'.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

After applying the fix, the corrected version of the function should correctly extract and format the Fish Shell version, resolving the bug and passing the failing test.