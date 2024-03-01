### Analysis:
- The `info` function in the `fish.py` file is using the command `echo $FISH_VERSION` to retrieve the Fish shell version, but the test is expecting the version to be obtained using `fish --version`.
- The test is mocking the `Popen` object to return the output `b'fish, version 3.5.9\n'` which corresponds to the output of `fish --version`.
- However, the function is currently reading the version from `echo $FISH_VERSION`, leading to a mismatch and causing the test to fail.

### Bug Fix Strategy:
- Update the `Popen` command in the `info` function to execute `fish --version` instead of `echo $FISH_VERSION`.
- Ensure that the function reads and processes the output correctly to get the Fish shell version in the expected format.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```