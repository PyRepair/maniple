### Potential Error Location:
- The issue seems to be with the command used to retrieve the Fish shell version.
- There might be a discrepancy between the command used to get the version and the actual output format, causing the test to fail.

### Bug Cause:
- The `info` function in the `fish.py` file is trying to get the Fish shell version by executing the command `echo $FISH_VERSION` using Popen.
- However, the test case is setting the expected output as `'Fish Shell 3.5.9'`, which differs from the actual output of the command.
- The test is expecting `'Fish Shell 3.5.9'`, but getting `'Fish Shell fish, version 3.5.9'`, resulting in the assertion error.

### Bug Fix Strategy:
- Update the command in the `info` function to match the version output provided by the test case.
- Use the correct command `['fish', '-c', 'echo $version']` to get the output `'fish, version 3.5.9'`.
- Modify the function to extract only the version number from the command output and format the return string accordingly.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

Now, the function should correctly extract the version number from the command output and return the formatted string `'Fish Shell 3.5.9'` as expected.