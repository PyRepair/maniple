### Analysis:
1. The `info` function in the `fish.py` file is attempting to get the version of the Fish shell by executing `fish -c 'echo $FISH_VERSION'`.
2. The failing test is mocking the subprocess call to return `b'fish, version 3.5.9\n'` when `Popen` is called with `['fish', '--version']`.
3. The error message indicates that the actual output from the function includes extra characters like `'fish, version'` while the expected output is `'Fish Shell 3.5.9'`.
4. The GitHub issue suggests that the current implementation causes a recursive loop when Oh-My-Fish plugin uses the `thefuck -v` command.

### Bug Explanation:
The bug is caused by the mismatch in the command used to get the Fish shell version. The function is trying to get the shell version using `echo $FISH_VERSION` instead of using `fish --version`. This results in incorrect parsing of the version string.

### Proposed Fix Strategy:
1. Modify the command in the subprocess call to `['fish', '--version']` to correctly retrieve the version of the Fish shell.
2. Parse the output of the subprocess call to extract the actual version number.

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8')
    version = version_output.strip().split(' ')[-1]
    return u'Fish Shell {}'.format(version)
``` 

With this fix, the function will correctly extract and return the version of the Fish shell, solving the bug and passing the failing test.