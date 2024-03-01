### Analysis
1. The `info` function in the `shells/fish.py` file is attempting to get the version of the Fish shell by executing a command using `Popen`. The expected output is `'Fish Shell X.X.X'` format but the current implementation is not extracting the version correctly.
2. The error message indicates that the actual output includes additional text `'fish, version 3.5.9'` which causes the assertion to fail when compared to the expected output `'Fish Shell 3.5.9'`.
3. The issue is related to the incorrect extraction of the version information from the shell command output. The function includes unnecessary text from the command output.
4. To fix the bug, we need to properly extract only the version number without any additional text.

### Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()  # Extract version correctly
    return u'Fish Shell {}'.format(version)
```

By splitting the command output using `,` and taking the second part after the split, we can correctly extract only the version number without any unnecessary text. This fix should address the bug and make the function return the expected output `'Fish Shell 3.5.9'`.