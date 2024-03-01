## Analysis
The `info` function in `fish.py` is attempting to retrieve the version of Fish Shell by running `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected version string is `'3.5.9'` while the actual output is `'fish, version 3.5.9'`. This discrepancy is causing the assertion error in the test.

The error occurs because the command `fish -c 'echo $FISH_VERSION'` does not return only the version number; it returns additional text as well, leading to the extra `'fish, '`. The `info` function is not handling this correctly.

## Strategy for Fixing the Bug
To fix the bug, we need to modify the `info` function to extract only the version number from the output of the command `fish -c 'echo $FISH_VERSION'`. We can achieve this by splitting the output string and extracting the version number.

## Corrected Version of the Function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number
    version = output.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this modification, the `info` function should now correctly extract only the version number after splitting the output string. This corrected version should pass the failing test case.