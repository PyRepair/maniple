### Analysis
- The `info` function is intended to retrieve the version of the Fish shell by executing the command `echo $FISH_VERSION`.
- The test case sets the expected output version to `Fish Shell 3.5.9`, but the function currently generates a version string in a different format.
- The function reads the output of the `echo $FISH_VERSION` command and formats it as `Fish Shell ${version}`, which is not the correct format based on the test case.
- The test case also expects the function to run the command `fish --version`, but the function actually runs `echo $FISH_VERSION`.

### Bug
The bug lies in the fact that the function is not executing the correct command to retrieve the Fish shell version and is not formatting the version string in the expected way.

### Strategy for Fixing the Bug
1. Update the command executed by `Popen` to `['fish', '--version']` to correctly retrieve the Fish shell version.
2. Update the formatting of the version string to match the expected output format `'Fish Shell X.X.X'`.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')  # Extract the version number from the output
    return 'Fish Shell {}'.format(version)
``` 

By making the above corrections, the function should now correctly retrieve the Fish shell version and format it as expected, passing the failing test.