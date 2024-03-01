### Bug Analysis:
The `info` function in the `fish.py` file is attempting to extract the version of the Fish shell using the command `echo $FISH_VERSION`. However, the actual output includes the text "fish, version 3.5.9" instead of just the version number. This causes the comparison in the test to fail as the expected value is only the version number without any additional text.

### Bug Location:
The bug is in the line where the version is being extracted from the command output:
```python
version = proc.stdout.read().decode('utf-8').strip()
```
This line is not correctly handling the command output to extract only the version number.

### Bug Cause:
The `version` variable is being set to the entire output of the command, which includes additional text ("fish, version") along with the actual version number. This causes the assertion in the test to fail as the expected value does not match the entire output.

### Fix Strategy:
To fix the bug, we need to modify the code to correctly extract only the version number from the output of the command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip()  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
```

By splitting the `version_output` at the comma and taking the second part (the version number) while removing any leading/trailing spaces, the corrected version will only return the version number without any additional text. This should make the function pass the failing test and resolve the issue reported on GitHub.