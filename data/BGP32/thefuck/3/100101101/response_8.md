## Analysis
The buggy function `info` is supposed to return the version of the Fish Shell by executing a command and extracting the version from the output. However, the command used to get the version (`echo $FISH_VERSION`) is incorrect, which leads to the wrong output. Additionally, the test is expecting the version number to be extracted correctly.

## Bug
The bug stems from the incorrect command `echo $FISH_VERSION`. Instead of directly getting the version number, this command returns the text `fish, version 3.5.9`. This mismatch causes the function to return the wrong version information, failing the test.

## Fix
To fix the bug, we need to update the command in the `Popen` call to `fish --version` to correctly extract the version number from the output.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

By updating the command to `fish --version`, the function will now correctly extract the version number from the output, fixing the bug and making the test pass.