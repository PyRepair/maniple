### Analysis:
1. The `info` function is supposed to return the version of the Fish shell by executing a command and capturing the output.
2. The test code sets up a mock scenario where the command output is simulated as `b'fish, version 3.5.9\n'`.
3. The function tries to read the output from the process, decode it, and format it into the desired string.
4. The runtime values show that the `Popen` object is a MagicMock, and the version string is correctly obtained.
5. The failing test indicates that the command used in `Popen` is incorrect, causing the function to return a version string that doesn't match the expected value.

### Bug Cause:
The `Popen` call in the `info` function is using `['fish', '-c', 'echo $FISH_VERSION']` to fetch the version, which is different from the expected command used in the failing test `['fish', '--version']`. This mismatch causes the function to return an unexpected version string.

### Strategy for Fixing the Bug:
1. Update the command executed by `Popen` to match the one used in the failing test to fetch the version correctly.
2. Make sure the decoding and formatting of the version string are handled appropriately.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

With this correction, the `info` function will execute the correct command to get the Fish shell version and format it to match the expected output, resolving the bug.