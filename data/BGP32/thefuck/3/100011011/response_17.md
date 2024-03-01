### Potential Error Locations:
1. The way the output is being read from `proc.stdout`.
2. The formatting of the version string.
3. The comparison between the expected output and the actual output.

### Explanation of the Bug:
The bug is likely due to the way the output from `proc.stdout.read()` is being handled. In the failing test case, the value of `version` is `'fish, version 3.5.9'` when it should be `'3.5.9'`. This discrepancy causes the assertion error because the expected output does not match the actual output of the function.

### Fix Strategy:
1. Modify the way the output is read from `proc.stdout` to extract only the version number.
2. Update the formatting of the version string to match the expected output.
3. Adjust the comparison between the expected output and the actual output to ensure they match.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip().replace('version ', '')
    return 'Fish Shell {}'.format(version)
```

By splitting the `version_output` and extracting only the version number, we ensure that the version string obtained matches the expected format. This corrected version should pass the failing test and resolve the issue reported on GitHub.