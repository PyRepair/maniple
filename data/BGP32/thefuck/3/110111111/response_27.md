To fix the bug in the `info` function of the `Fish` class, we need to adjust the command being run to retrieve the version of Fish shell. The current command `echo $FISH_VERSION` may not return the version directly and might include additional information causing the assertion error in the test.

### Bug Explanation:
- The `info` function is using the command `echo $FISH_VERSION` to retrieve the version of Fish shell, which is not returning the version number in the expected format.
- This discrepancy leads to the assertion error in the test where the actual output includes additional information like `fish, version`.
- The test is expecting only the version number, for example, `3.5.9`, without any extra text.

### Fix Strategy:
- Modify the command being executed in the `info` function to directly return the version number of Fish shell without any additional text.
- Update the function to extract only the version number from the command output.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        
        version = proc.stdout.read().decode('utf-8').strip().split()[2]
        return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']` and extracting the version number correctly from the command output, the corrected version of the `info` function should now pass the failing test with the expected output.