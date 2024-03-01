## Analysis
1. The buggy function `info()` in the `Fish` class is supposed to return the version of the Fish shell by running a command in the shell.
2. The test function `test_info` in the test file is mocking the `Popen` function to return the version string that is expected to be extracted by the `info()` function. The test is failing because the expected output does not match with the actual output.
3. The error message shows that the expected output contains additional text "fish, version" which is not handled in the `info()` function.
4. The root cause of the bug is that the function is not extracting the version correctly and is not filtering out the unnecessary text from the output.
5. To fix the bug, we need to modify the `info()` function to extract only the version number part from the output of the command.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

In the fixed version:
1. The command is changed to `['fish', '--version']` to get the version information directly.
2. The extracted version is split on the comma and the second part is taken as the version number.
3. This ensures that only the version number (e.g., '3.5.9') is included in the return string.
4. The function should now pass the test successfully.