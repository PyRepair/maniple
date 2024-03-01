### Analysis
- **Error Message:** The assertion error shows that the function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
- **Runtime Values:** The `version` variable contains the entire string `'fish, version 3.5.9'`.
- **Expected Values:** The expected value for the `version` variable is `'3.5.9'`.
- **GitHub Issue:** The issue relates to a problem with the `-v` flag in Oh-My-Fish plugin causing a recursive loop due to the buggy function.

### Bug Location
The bug is primarily in the way the output is processed from `proc.stdout.read()`. It is not correctly extracting just the version number from the output.

### Bug Cause
The bug is caused by the function not properly parsing the version number from the command output. This results in the entire string being used in the output, leading to the assertion error.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the way the version number is extracted from the output. We should only take the version number without the unnecessary text.

### Corrected Code
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output and considering only the last element of the split, we extract just the version number. This correction ensures that the function returns the expected output and resolves the issue reported on GitHub.