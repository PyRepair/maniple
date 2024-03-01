### Bug Analysis
1. The buggy function `info` in the `fish.py` file of the `thefuck` module is attempting to retrieve the version of the Fish shell but it includes unnecessary text along with the version number.
2. The error message from the failing test indicates that the expected output is `'Fish Shell 3.5.9'` but the actual output contains additional text, resulting in the assertion error.
3. The key issue originates from the fact that the function is not properly parsing the version number from the shell command output.
4. To fix this bug, the function needs to extract only the version number from the command output and format it correctly to match the expected output.

### Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(",")[1].strip()  # Extract only the version number
    return 'Fish Shell {}'.format(version)
```

After implementing this fix, the function should now correctly extract and format the version number from the shell command output, resolving the bug.