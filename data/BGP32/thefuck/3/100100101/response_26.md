### Analysis
1. The `info` function is supposed to retrieve the version of the Fish shell by executing a command and capturing the output.
2. The function uses `Popen` to run the command `'fish -c 'echo $FISH_VERSION'` and capture the output.
3. The `test_info` test case sets the expected output to be `'fish, version 3.5.9\n'` and expects the function to return `'Fish Shell 3.5.9'`.
4. The issue lies in the command being executed in the `Popen` call, which is `'echo $FISH_VERSION'` instead of `fish --version`.

### Bug Explanation
- The command `echo $FISH_VERSION` does not retrieve the correct version string as expected by the test case.
- As a result, the function fails to provide the correct version of the Fish shell.

### Bug Fix
To fix the bug, update the command executed by `Popen` to `'fish --version'`, which will properly fetch the version information.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extracting the version number
    return u'Fish Shell {}'.format(version)
```