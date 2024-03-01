The bug in the provided `info` function is due to the mismatch in the command used to retrieve the Fish shell version and the command being checked in the test function.

### Error Location:
The error location is in the command being executed in the Popen call in the `info` function. The command to retrieve the Fish shell version should be `'echo $FISH_VERSION'` instead of `'--version'`.

### Cause of the Bug:
The test function is setting up the `Popen` return value to simulate the output of `'fish, version 3.5.9\n'`, which is incorrect because the `info` function is trying to retrieve the version by executing `'echo $FISH_VERSION'`.

### Strategy for Fixing the Bug:
To fix the bug, we should update the command being executed in the `Popen` call of the `info` function to `'echo $FISH_VERSION'` to retrieve the correct Fish shell version.

### Corrected Version of the `info` Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell {}'.format(version)
```

By updating the command in the `info` function as shown above, the provided failing test should now pass.