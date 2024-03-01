### Analysis:
1. The `info` function in the `fish.py` file is supposed to retrieve the version of the Fish Shell by executing the command `fish -c 'echo $FISH_VERSION'`. However, the command being executed in the test is `['fish', '--version']`, which is incorrect.
2. The function reads the output of the process incorrectly and fails to extract only the version number from the output.

### Bug Cause:
The main causes of the bug are:
1. Incorrect command execution in the `info` function.
2. Improper handling of the output of the executed process.

### Fix Strategy:
1. Update the command used in the Popen call to fetch the Fish Shell version correctly.
2. Modify the parsing of the output to extract and return only the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[2]  # Extract the version number
    return u'Fish Shell {}'.format(version)
```

By making the above changes, the corrected function should now properly retrieve and return the version of the Fish Shell, resolving the issue and passing the failing test.