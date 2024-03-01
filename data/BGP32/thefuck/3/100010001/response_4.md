### Analysis:
1. The buggy function `info` is trying to get the version of the Fish shell by running a command in a subprocess (`Popen`).
2. The error message shows that the version retrieved from the command contains extraneous characters (`'fish, version 3.5.9\n'`) which causes the assertion to fail.
3. The issue is caused by the incorrect formatting of the `echo $FISH_VERSION` command output.
4. To fix the bug, we need to adjust the command to only output the version number without any extra characters.

### Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    # Extract version number from the command output
    version = output.split(',')[1].strip()  # Extracts the version number part
    return u'Fish Shell {}'.format(version)
```

### Explanation:
1. The fixed version of the function splits the output of the command by comma and takes the second part (the version number).
2. This ensures that only the version number is considered, eliminating the extraneous characters causing the assertion failure.
3. The corrected version of the function should now pass the failing test by providing the expected output, 'Fish Shell 3.5.9'.