### Analysis
1. The function `info` fetches the version of the Fish shell by running a command in a subprocess.
2. The function then reads the output of the subprocess and extracts the version number.
3. The current implementation is fetching the version using `echo $FISH_VERSION` in the subprocess, while the test expects the version to be fetched using `fish --version`.
4. This discrepancy in the command used in the subprocess is causing the function to return the wrong version number and fail the test.

### Bug
The bug in the current function is due to not using the correct command (`fish --version`) to fetch the version of the Fish shell. This causes the function to return an incorrect version number, leading to a failing test.

### Strategy for Fixing the Bug
To fix the bug, we need to update the command passed to the subprocess to correctly fetch the Fish shell version.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

By updating the command to `['fish', '--version']`, the function will now correctly fetch the version of the Fish shell. The corrected function should now pass the failing test and provide the expected output.