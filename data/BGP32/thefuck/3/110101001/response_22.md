### Bug Explanation
The buggy function is trying to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using the `Popen` function. However, in the failing test scenario, the expected output is `'fish, version 3.5.9\n'`, which does not match the output retrieved by the function.

The root cause of the bug is that the command `echo $FISH_VERSION` does not return the correct version number in the expected output format.

### Bug Fix Strategy
To fix the bug, we need to modify the command being run by `Popen` to correctly retrieve the Fish shell version information in the expected format.

### Corrected Version
```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # extract version number from the output
        version = version.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

By changing the command to `['fish', '--version']`, we ensure that the correct version information is being retrieved from the output. Additionally, we split the output by `,` to extract only the version number part and remove any unnecessary text.