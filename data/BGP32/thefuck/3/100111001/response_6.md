### Identified issues:
1. The command being executed in the `Popen` call is `['fish', '-c', 'echo $FISH_VERSION']`, but the test expects the version to be extracted from the output of `fish --version`.
2. The `Popen.return_value.stdout.read.side_effect` is set to `b'fish, version 3.5.9\n'`, but the function does not handle this specific format correctly.

### Bug cause:
The bug is caused by the mismatch between the command executed in the `Popen` call and the expected output format in the test. Additionally, the function does not strip the unnecessary characters from the obtained version string.

### Strategy for fixing the bug:
1. Update the command in the `Popen` call to execute `fish --version` instead of retrieving the version.
2. Modify the function to correctly handle the format of the version string extracted from the output.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By making these changes, the function will extract the version correctly from the output of `fish --version` and return the value as expected by the test.