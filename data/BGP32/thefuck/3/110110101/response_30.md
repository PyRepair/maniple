### Fixing the Bug in the `info` Function

#### Analysis:
- The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell by executing `fish -c 'echo $FISH_VERSION'` command.
- The test case expects the output to be in the format `'Fish Shell 3.5.9'`.
- The error in the current implementation is related to how the version is fetched and formatted.

#### Bug Cause:
- The version extraction logic from the command output is incorrect.
- Instead of getting only the version number, the command result includes additional text like `fish, version`.
- This discrepancy causes the assertion error in the test case.

#### Fix Strategy:
- Adjust the logic to extract only the version number from the command output.
- Update the formatting to match the expected output format `'Fish Shell x.x.x'`.

#### Corrected Version of the `info` Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()  # Extract version from the command output
    return 'Fish Shell {}'.format(version)
```

By using the corrected version above, the function should now properly extract the version number and format it according to the expected output. This will ensure that the test case passes successfully.