### Analysis:
1. The buggy function `info` in the `Fish` class attempts to retrieve the version of Fish shell using `Popen` and then format the output.
2. The failing test `test_info` sets up the `Popen` mock to return a specific version string and asserts that the `info` function correctly formats this version.
3. The error message indicates that the expected output is not matching the actual output due to extra characters in the version string.
4. The bug causes the version string to include extra characters leading to the assertion failure.
5. The suggested strategy for fixing the bug involves modifying the way the version string is retrieved and formatted.

### Bug cause:
The bug is caused by incorrect parsing of the version output string from the Fish shell. It includes extra characters like "fish, version" which should not be part of the final version string.

### Suggested Fix:
1. Modify the command used by `Popen` to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to directly get the version information.
2. Update the parsing logic to extract just the version number without any additional characters.
3. Update the `info` function to consider these changes for correct output.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extracting just the version number
    return f'Fish Shell {version}'  # Using f-string for formatting
```

By making the above changes in the `info` function, it should now correctly extract the version number and format it as expected. This fix will resolve the issue reported on GitHub and pass the failing test without any extra characters in the output.