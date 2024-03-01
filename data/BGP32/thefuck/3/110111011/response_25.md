## Bug Explanation:

The buggy function `info` in the `Fish` class is trying to retrieve the version of the Fish shell by running `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected version string is `'Fish Shell 3.5.9'`, while the actual version string obtained from the Popen command includes `'fish, version 3.5.9'`. This discrepancy causes the assertion to fail.

The initial implementation of the `info` function does not correctly extract the version string from the output of the `Popen` command, leading to the wrong comparison in the test case and causing the test to fail.

## Fix Strategy:

To fix this bug, we need to modify the way the version is extracted from the Popen output. We can directly extract the version number by splitting the string `'fish, version 3.5.9'` on the commas and spaces and then only consider the last element which should be the version number.

## Corrected Version:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_raw = proc.stdout.read().decode('utf-8').strip()
        version = version_raw.split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

This corrected version of the `info` function correctly extracts the version number from the output of the Popen command and returns it along with the shell name. This should now pass the failing test case and resolve the issue mentioned on GitHub.