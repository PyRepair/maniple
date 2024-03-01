### Explanation:
The bug in the current function is causing the returned version string to include unnecessary text ("fish, version") along with the actual version number. This discrepancy is causing the assertion error in the failing test.

The function is reading the output of the process directly using `proc.stdout.read()`, which includes the entire output string "fish, version 3.5.9". To fix this bug, we need to extract only the version number from the output string.

### Strategy for fixing the bug:
1. Instead of directly reading the output using `proc.stdout.read()`, we can split the output string by spaces and extract the version number from it.
2. By splitting the output and selecting the appropriate index that contains the version number, we can ensure that the returned string only includes the version number without any extra text.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1]  # Extract the last element as the version number
    return u'Fish Shell {}'.format(version)
``` 

By making this change, the function will now correctly extract and return only the version number without any additional text, fixing the bug and passing the failing test.