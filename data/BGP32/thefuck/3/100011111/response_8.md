### Bug Analysis
The issue lies in the `info` function where the `version` variable is set to the output of the command `'echo $FISH_VERSION'`. However, the output includes the text `'fish, version'` which is not desired. This causes the assertion error as the expected result does not include the text `'fish, version'`.

### Bug Fix Strategy
To fix the bug, we need to extract only the version number from the output of the command `'echo $FISH_VERSION'` before constructing the return string. We can achieve this by parsing the output string to extract the version number.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1]  # Extracting the version number from the output
    return u'Fish Shell {}'.format(version)
```

By extracting only the version number from the output before returning, the corrected function will now provide the expected output without the additional text, resolving the assertion error in the failing test.