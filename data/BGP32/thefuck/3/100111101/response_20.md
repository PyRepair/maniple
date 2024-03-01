### Analysis
1. The `info` function in the `Fish` class is supposed to return the version of the Fish shell by executing a command. However, the command used to get the version is incorrect (`echo $FISH_VERSION`).
2. The failing test sets up the `Popen` mock to return the output of `fish --version`, which the `info` function should be using.
3. The error message shows that the expected output of the `info` function is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This indicates that the incorrect command is being used to fetch the version.
4. To fix the bug, we need to update the command being executed in the `Popen` call to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

### Updated Code
```python
# The relative path of the buggy file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()

    # Extract the version number from the output
    version = version.split(', version ')[1]

    return u'Fish Shell {}'.format(version)
```

By updating the `info` function as shown above, the command executed to get the Fish shell version is now correct. It should now return the expected version format and pass the failing test case.