### Fixing the bug in the `info` function

#### Bug in the current implementation:
1. The `info` function is trying to extract the fish version using the command `'echo $FISH_VERSION'`, which is incorrect.
2. The test is setting up the expected output as `'Fish Shell 3.5.9'`, but the actual output contains additional text `'fish, version 3.5.9'`.
3. The assertion error occurs because the actual output does not match the expected output.

#### Fix strategy:
1. Update the command to `'fish --version'` to correctly retrieve the version information.
2. Modify the output parsing logic to extract only the version number.
3. Update the comparison in the test to match the modified output.

#### Corrected version of the `info` function:
```python
# The corrected version of the info function in the Fish class
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[2]
        return u'Fish Shell {}'.format(version)
```

With this corrected version, the function now properly retrieves the fish shell version using the `'fish --version'` command and extracts only the version number for comparison with the expected output.

### Updated test assertion:
```python
# Updated test assertion
assert shell.info() == 'Fish Shell 3.5.9'
``` 

By making these changes, the `info` function should now return the correct version information and pass the failing test.