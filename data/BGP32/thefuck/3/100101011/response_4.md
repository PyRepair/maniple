### Analysis
The `info` function in the `fish.py` file is supposed to return the name and version of the current Fish shell by running the command `echo $FISH_VERSION`. However, the failing test shows that the expected output ('Fish Shell 3.5.9') does not match the actual output ('fish, version 3.5.9'). This indicates a mismatch in the command execution and processing of the shell version.

### Bug Cause
The bug is caused by the incorrect command used to fetch the Fish shell version. The command in the `Popen` call is `['fish', '-c', 'echo $FISH_VERSION']`, whereas the test expects the version output from `['fish', '--version']`. This mismatch results in the incorrect version string being fetched.

### Fix Strategy
To fix the bug, we need to update the command executed within the `Popen` call to fetch the Fish shell version using `['fish', '--version']`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extract the version number only
    return 'Fish Shell {}'.format(version)
```

With this corrected version of the `info` function, it will fetch the Fish shell version correctly using `['fish', '--version']`, which aligns with the expected output in the failing test case.