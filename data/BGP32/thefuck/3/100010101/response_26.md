### Analysis
- The buggy function `info` is using `Popen` to run a command in the fish shell and retrieve the version number.
- The error message indicates that the function is returning an unexpected string format for the version number.
- The expected version number is `'3.5.9'`, but the function is returning `'fish, version 3.5.9'`.
- The cause of the bug is that the function is not correctly parsing the output of the command to extract only the version number.
- The `strip()` function is not handling the output properly, resulting in the unexpected format.
- To fix the bug, we need to modify how the version number is extracted from the command output.

### Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return 'Fish Shell {}'.format(version)
``` 

### Explanation
- In the fixed version, we use the `split(', version ')` function to separate the output string and extract only the version number.
- By using this approach, we ensure that the extracted version number is in the correct format ('3.5.9') as expected.