### Analysis:
1. The `info` function is attempting to capture the fish shell version by executing a command and reading the output.
2. The failing test is asserting that the captured version matches the expected version 'Fish Shell 3.5.9', but there is an additional prefix 'fish, version' in the actual captured output.
3. The error message shows the actual and expected versions, highlighting the difference between them.
4. The bug is likely due to the command being executed returning 'fish, version 3.5.9' instead of just the version number.
   
### Strategy for Fixing the Bug:
- It seems that the command issued to obtain the shell version (`echo $FISH_VERSION`) is returning additional text along with the version number.
- To fix the bug, we need to modify the command or extract the version number correctly from the output.
- We should modify the `info` function to properly parse the output and extract only the version number.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()  # Extract the version from the output
    return u'Fish Shell {}'.format(version)
```

By modifying the command to `['fish', '--version']` and extracting and trimming the version number correctly, we can fix the bug and have the function return the expected shell version.