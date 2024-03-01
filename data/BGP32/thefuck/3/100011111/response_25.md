### Analysis
The buggy function `info` is trying to get the version of the Fish shell by executing a command through `Popen` and then reading the output. However, the current implementation does not correctly extract only the version number from the output, leading to the assertion error in the failing test.

### Error Explanation
- The failing test provides expected version number `3.5.9`, but the actual output contains the text `'fish, version 3.5.9'`.
- The buggy function is directly returning the entire output string after converting it to Unicode and formatting it, resulting in the version number preceded by `'Fish Shell'`.

### Fix Strategy
To fix the bug, we need to modify the function such that it properly extracts just the version number from the command output before formatting and returning the string.

### Correction
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_text = proc.stdout.read().decode('utf-8').strip()
    version_number = version_text.split(", version ")[1]  # Extract version number
    return f'Fish Shell {version_number}'
``` 

This corrected version of the `info` function now correctly extracts the version number from the output of the `echo $FISH_VERSION` command before formatting and returning it as part of the shell name.