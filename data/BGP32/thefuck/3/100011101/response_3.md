### Bug Explanation
The bug in the provided function `info` is due to the incorrect formatting of the `version` string obtained from the `fish -c 'echo $FISH_VERSION'` command. The `version` variable retains the whole string `'fish, version 3.5.9'` instead of just the version number `'3.5.9'`. This causes the assertion error as the expected output is `'Fish Shell 3.5.9'`.

### Fix Strategy
To fix this bug, we need to extract only the version number from the obtained string. One way to achieve this is by splitting the string based on the delimiter `', version '`, and then using the second part of the split result as the version number.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
```

By making this correction, the function should now correctly extract the version number and return the expected output `'Fish Shell 3.5.9'`.