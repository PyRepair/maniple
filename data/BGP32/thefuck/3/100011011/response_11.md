### Analysis:
1. The `info` function is supposed to return the version of the Fish shell by running a command in a subprocess and extracting the version from the output.
2. The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes the word `'fish, version'` in addition to the version number.
3. The provided runtime values and types show that the `version` variable contains the entire output of the command, including the unnecessary text `'fish, version'`.
4. The bug seems to be related to the parsing of the version number from the output of the subprocess command.

### Bug:
The bug in the function is that it does not correctly parse the version number from the output of the subprocess command, resulting in unnecessary text being included in the return value.

### Fix:
To fix the bug, we need to modify the code to extract only the version number from the output and format the return string accordingly.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we split the output of the subprocess command by spaces and extract the third element (index 2) which represents the version number. This change ensures that only the version number is included in the return value.