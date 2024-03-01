### Bug Explanation
The bug in the `info` function is due to the incorrect command used to get the Fish shell version. The command `echo $FISH_VERSION` does not return the version information in the desired format. Additionally, in the test case, the expected version number is '3.5.9', but the provided command in the function does not extract this exact information.

### Strategy for Fixing the Bug
To fix the bug, we need to change the command used to retrieve the Fish shell version and update the function accordingly. We should modify the command to retrieve the version number directly using `fish --version`.

### Corrected Function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split()[-1]  # Extract the version number from the command output
    return f'Fish Shell {version}'
```

By updating the function with the corrected command to get the Fish shell version and correctly extract the version number, the function should now pass the failing test case.