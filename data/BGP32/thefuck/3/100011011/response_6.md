### Analysis:
1. The error message indicates that the expected output is `'Fish Shell 3.5.9'` but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the `info` function is not correctly formatting the version string.
2. The `Popen` mock object is returning `'fish, version 3.5.9'` which is being processed incorrectly in the function.
3. The function is reading the output of the `Popen` process and directly using it as the version without properly parsing and formatting it.
4. To fix this bug, we need to parse the output of the `Popen` process to extract only the version number.

### Strategy for Fixing the Bug:
1. Since the version is returned as `'fish, version 3.5.9'`, we need to extract only the version number.
2. To do this, we will split the output string based on `' '` (space), take the last element after the split, and then extract the part after `'version'`.
3. We will then format this correctly to get the desired output `'Fish Shell 3.5.9'`.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1].split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

By parsing the version string properly, the corrected function should now output `'Fish Shell 3.5.9'` as expected.