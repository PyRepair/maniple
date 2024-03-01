## Analyzation
1. The buggy function `info` attempts to retrieve the version of the Fish shell by executing `fish -c 'echo $FISH_VERSION'`. However, the function is not correctly parsing the output to extract only the version number.
2. The error message shows that the actual output contains `'fish, version 3.5.9'` instead of just `'3.5.9'`.
3. The function is supposed to return the version of Fish shell with the format `'Fish Shell {version}'`. In this case, it failed to strip the unnecessary part from the version string.
4. To fix the bug, we need to modify the parsing logic to extract only the version number from the output.

## Solution
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(",")[1].strip()
    return u'Fish Shell {}'.format(version)
```

By splitting the output on the comma and retrieving the second part after splitting, we can extract only the version number without any additional text. This change will ensure that the function returns the correct version number format as `'Fish Shell {version}'.`