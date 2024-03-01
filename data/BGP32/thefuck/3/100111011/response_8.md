Based on the provided information, the bug in the `info` method of the `Fish` class in `fish.py` is due to the incorrect command being used to retrieve the Fish version, leading to a mismatch in the expected output from the test function.

### Identified Issue:
1. In the `info` function, the command `echo $FISH_VERSION` is being used to extract the Fish shell version. However, the test is expecting the version to be retrieved using the `fish --version` command.
2. This discrepancy causes the `proc.stdout.read().decode('utf-8').strip()` method to result in `'fish, version 3.5.9'` instead of just `'3.5.9'`.

### Fix Strategy:
1. Update the command in the `Popen` call to use `fish --version` instead of `echo $FISH_VERSION`.
2. Modify the parsing of the version string to extract only the version number, excluding any extraneous text.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()  # Extract just the version number
    return u'Fish Shell {}'.format(version)
```

By making these changes, the function will correctly extract and return the Fish shell version, aligning with the expectations of the test function. This correction should address the failing test case and resolve the GitHub issue related to the recursive loop.