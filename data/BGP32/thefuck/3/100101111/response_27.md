### Explanation:
The bug in the `info` function of the `Fish` class arises from reading the `FISH_VERSION` environment variable instead of parsing the actual version information from the output of `fish --version` command. This causes the version string to include unnecessary text like "fish, version" in addition to the version number.

Additionally, the assertion in the failing test (`test_info`) expects the command to be `['fish', '--version']` while the actual command used is `['fish', '-c', 'echo $FISH_VERSION']`.

### Proposed Fix:
To fix this bug, we need to modify the `info` function to execute the correct command (`['fish', '--version']`) to extract the shell version and then parse it to get only the version number. We should also correct the command used in the test to align it with the expected behavior.
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extract version number
    return u'Fish Shell {}'.format(version)
```

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]  # Extract version number
    return u'Fish Shell {}'.format(version)
```

By making these changes, the `info` function will correctly extract and display only the version number of the Fish shell, resolving the bug and aligning it with the expected behavior.