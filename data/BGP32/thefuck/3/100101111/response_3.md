### Analysis
1. The `info` function is attempting to retrieve the Fish shell version by running a subprocess command. However, it's using the wrong command to get the version (`'echo $FISH_VERSION'` instead of `'fish --version'`) which leads to incorrect output.
2. The failing test is setting the expected output to `'fish, version 3.5.9\n'`.
3. The bug occurs because the subprocess output is not parsed correctly to extract just the version number.
4. To fix the bug, the function needs to execute the correct subprocess command and then parse the output to extract the version number.

### Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split()[2]
    return f'Fish Shell {version}'
``` 

### Explanation
- Changed the subprocess command in `Popen` to `['fish', '--version']` to correctly retrieve the version.
- Read the stdout output from the subprocess, stripped any extra spaces or newlines.
- Extracted the version number by splitting the output at spaces and selecting the third element.
- Formatted the return string to include the extracted version number.

By applying this fix, the `info` function should now correctly extract and return the Fish shell version, passing the failing test case and fixing the bug reported in the GitHub issue.