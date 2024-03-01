### Analysis:
1. The buggy function, `info`, is supposed to return the name and version of the current shell by executing a command `echo $FISH_VERSION` in a subprocess.
2. The failing test `test_info` mocks the subprocess behavior by setting `Popen.return_value.stdout.read.side_effect` to simulate the output of the command.
3. The error message indicates that the expected output `'Fish Shell 3.5.9'` does not match the actual output `'Fish Shell fish, version 3.5.9'`.
4. The bug seems to be caused by incorrect parsing of the version string received from the command output.
5. To fix the bug, we need to properly extract and format the version string in the `info` function.

### Strategy for fixing the bug:
1. Update the `Popen` command to read the version information with the correct command, i.e., `fish --version`, instead of just `echo $FISH_VERSION`.
2. Parse the correct version information and format it correctly before returning.

### Corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_str = version.split(',')[1].strip()
    return f'Fish Shell {version_str}'
```

By updating the `Popen` command and correctly parsing the version information using `split` and `strip`, the corrected version of the `info` function should now pass the failing test case.