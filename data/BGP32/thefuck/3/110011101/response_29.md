### Analysis
The bug in the `info` function is that the version string retrieved from the `fish` shell includes unnecessary information ('fish, version') that should be removed before formatting the final output. This is causing the assertion error as the expected output is missing this unnecessary information.

### Bug Cause
The cause of the bug is that the code snippet `b'fish, version 3.5.9\n'` is being read as the output from `fish -c 'echo $FISH_VERSION'`. The unnecessary prefix 'fish, version' is included in the version string, leading to a mismatch in the expected and actual values at the time of comparison.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the code to extract only the version number from the output string. We can achieve this by stripping the unnecessary prefix 'fish, version' before formatting the final output.

### Corrected Version of the Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        # Extract version number by removing 'fish, version ' prefix
        version = version_output.replace('fish, version ', '')
        return u'Fish Shell {}'.format(version)
``` 

By removing the unnecessary prefix 'fish, version ' from the version string, the corrected function will now return the expected output 'Fish Shell 3.5.9'. This will ensure that the assertion passes and the bug is fixed.