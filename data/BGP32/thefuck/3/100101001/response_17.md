## Bug Analysis
The buggy function `info` is supposed to return the version of the Fish shell by executing a command in a subprocess. However, there are several issues causing the test to fail:
1. The command being executed is `echo $FISH_VERSION`, but the test is expecting the command `fish --version`.
2. The `Popen` call doesn't match the expected arguments in the test.
3. The reading of stdout from the process is not handled correctly.

## Bug Fix Strategy
To fix the bug:
1. Adjust the command being executed to retrieve the Fish shell version correctly.
2. Update the `Popen` call to match the arguments expected in the test.
3. Properly read and decode the stdout output from the process.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
``` 

In the corrected version:
- The command executed is `fish --version` to retrieve the correct version.
- The `Popen` call is updated to match the expected arguments in the test.
- The stdout is read using `readline()` method and properly decoded and stripped to extract the version information.