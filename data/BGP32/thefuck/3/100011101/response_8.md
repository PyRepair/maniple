### Analysis
The issue in the buggy function lies in the way it retrieves the version information from the output of the `fish -c 'echo $FISH_VERSION'` command. The version information extracted includes the text "fish, version" along with the actual version number, which causes the discrepancy in the assertion.

### Bug Explanation
The current implementation of the `info` function extracts the version information as `'fish, version 3.5.9'` instead of just the version number `'3.5.9'`. This additional text causes the assertion to fail as it is not equal to the expected output `'Fish Shell 3.5.9'`.

### Fix Strategy
To fix this bug, we need to modify the function to extract only the version number from the output string. We can achieve this by splitting the output string based on the delimiter `', version '` and taking the second part of the split as the version number.

### Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this modification, the `info` function will correctly extract the version number from the output, resulting in the expected output of `'Fish Shell 3.5.9'`.