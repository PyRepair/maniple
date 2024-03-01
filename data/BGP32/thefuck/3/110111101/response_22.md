### Explanation:
The bug in the `info` function is due to the incorrect command used to retrieve the version of the Fish shell. The command `'echo $FISH_VERSION'` does not match the expected output that the test is looking for (`'fish, version 3.5.9'`). This causes the assertion to fail because the version fetched is not in the correct format.

### Solution:
- Update the command in the `Popen` call to `'fish', '--version'` to match the expected output format.
- Modify the parsing logic to extract the version number correctly.

### Corrected Version:
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[-1].strip()  # Extract version from the output
        return u'Fish Shell {}'.format(version)
```