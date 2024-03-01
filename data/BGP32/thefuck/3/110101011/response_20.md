### Analysis:
1. The buggy function `info` in the `Fish` class is supposed to return the version of the Fish Shell by running a subprocess command. However, it seems to be using an incorrect command `echo $FISH_VERSION` instead of `fish --version`.
 
2. The failing test `test_info` expects the output to be `'Fish Shell 3.5.9'` but is currently failing due to the incorrect command used in the `info` function.

### Bug Cause:
The bug seems to be caused by the incorrect subprocess command used to retrieve the version of the Fish Shell within the `info` function. This leads to the function not returning the expected version number, causing the test to fail.

### Fix Strategy:
To fix the bug, we need to update the subprocess command within the `info` function to correctly get the version of the Fish Shell.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(', version ')[1].rstrip('\n'))
```

By updating the subprocess command in the `info` function to `['fish', '--version']`, we ensure that the correct version of the Fish Shell is obtained. Additionally, the returned version is modified to extract only the version number without any extra characters. This corrected version should now pass the failing test and resolve the issue reported on GitHub.