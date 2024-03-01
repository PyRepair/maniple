### Analysis:
1. The buggy function `info` is supposed to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and then formatting the output.
2. The failing test expects the version string `'3.5.9'`.
3. The error occurs because the extracted version string includes extra information "fish, version" that needs to be removed before formatting.
4. To fix the bug, we need to modify the logic to extract only the version number without the additional text.

### Correction:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version.strip(','))
``` 

By modifying the `version` assignment to extract only the last element obtained after splitting the string by whitespace, the bug is fixed. Now, the function should return the correct version number without the extra text.