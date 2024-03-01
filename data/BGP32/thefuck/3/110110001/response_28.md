### Explanation:
1. The buggy function `info` in the `Fish` class is supposed to return the name and version of the Fish shell. It currently calls the `Popen` function to execute a command (`echo $FISH_VERSION`) and read the output to get the version. However, the command executed does not match the expected version output format that the test is asserting against.

### Bug Location:
The bug is in the `info` function where the command `echo $FISH_VERSION` is being executed to get the version.

### Cause of the Bug:
The actual version output (`'fish, version 3.5.9\n'`) from the command is different from what the test function expects (`'Fish Shell 3.5.9'`). This causes the assertion in the test to fail.

### Strategy for Fixing:
To fix the bug, modify the command being executed in `Popen` to get the correct version output format. Also, update the assertions in the test to match the new expected output.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return f'Fish Shell {version.replace("fish, version ", "")}'
```

In this corrected version, the correct command (`['fish', '--version']`) is being executed to get the version output, and the obtained version is reformatted to match the expected output format in the test.