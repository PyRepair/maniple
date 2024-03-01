### Analysis
The `info` function is intended to return the name and version of the current Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. However, the test is failing because the expected version string is `'fish, version 3.5.9'` while the function is currently not parsing it correctly.

The GitHub issue reveals that the issue is related to the use of the `thefuck -v` command and the interaction with the Oh-My-Fish plugin. The function needs to correctly extract the version information to avoid the recursive loop caused by the plugin.

### Bug
The bug in the current implementation arises from the incorrect parsing of the version output. The function is not correctly extracting the version number from the command output. It should extract the version number '3.5.9' instead of 'fish, version 3.5.9'.

### Fix Strategy
To fix the bug, modify the function to correctly parse and extract the version number from the command output. Remove any unnecessary characters and whitespace to obtain the desired version format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output on `', '` and extracting the second part, which contains the version number, we can fix the bug and ensure that the function returns the correct version information.