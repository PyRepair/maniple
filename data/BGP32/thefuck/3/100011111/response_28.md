### Bug Explanation
The bug in the `info` function of the `Fish` class in `fish.py` is related to the incorrect parsing of the version string from the output of the `fish -c 'echo $FISH_VERSION'` command. The function is returning 'Fish Shell' followed by the entire output of the command, including 'fish, version'. This causes the assertion error in the failing test.

The expected behavior is to extract only the version number (e.g., '3.5.9') from the command output and include it in the return string.

### Bug Fix Strategy
To fix the bug, we need to modify the parsing logic of the version string obtained from the `fish -c 'echo $FISH_VERSION'` command. We should extract and format only the version number from the output and include it in the return string.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract only the version number by splitting the output on ','
    version_parts = version.split(',')
    version_number = version_parts[1].strip()
    
    return u'Fish Shell {}'.format(version_number)
```

The corrected version of the function parses the version string correctly and returns 'Fish Shell' followed by the extracted version number. This corrected version should pass the failing test and satisfy the expected input/output values, resolving the issue mentioned in the GitHub report.