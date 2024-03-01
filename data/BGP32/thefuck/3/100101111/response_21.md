### Analysis
The bug in the `info` function is related to the command used to fetch the Fish Shell version. The `echo $FISH_VERSION` command is returning extra text "fish, version" along with the actual version number. This mismatch causes the test to fail.

### Bug Cause
The `info` function fetches the Fish Shell version by running the command `echo $FISH_VERSION`, and then it reads the output to get the version number. However, the output of this command includes additional text "fish, version" before the actual version number. This additional text causes the comparison in the test to fail since it expects just the version number. Hence, the function needs to be modified to only extract the version number from the output.

### Bug Fix
To fix the bug, we need to modify the function to extract only the version number from the output of the command. We can achieve this by splitting the output string and extracting the relevant part before constructing the return string.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_number = version.split(', version ')[1]  # Extract only the version number
    return u'Fish Shell {}'.format(version_number)
```

After applying this fix, the `info` function will correctly extract just the version number from the output of the command, and the test case provided should pass successfully.