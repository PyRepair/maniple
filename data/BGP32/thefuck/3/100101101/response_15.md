#### Analysis:
The buggy function is trying to extract the version of the Fish shell by executing `echo $FISH_VERSION` using the subprocess module. However, the test is providing the version number as `fish, version 3.5.9`, which includes extra text that needs to be stripped out.

#### Bug:
The bug is caused by not stripping out the extra text `fish, version` from the version number extracted from the subprocess output.

#### Fix:
To fix the bug, we need to modify the function to extract only the version number from the output.

#### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
    return u'Fish Shell {}'.format(version)
```