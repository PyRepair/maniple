#### Bug Explanation:
The bug in the `info` function of the `Fish` class lies in how the version string is extracted from the `fish -c 'echo $FISH_VERSION'` command output. The test is expecting the version number to be extracted correctly, but the current implementation includes additional text (`fish, version`) in the output, causing the test to fail.

The runtime input/output values show that the `version` variable contains `'fish, version 3.5.9'`, whereas the expected output should be `'3.5.9'`.

#### Fix Strategy:
To fix the bug, we need to modify the way the version string is extracted to only include the version number without any additional text.

#### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return u'Fish Shell {}'.format(version)
``` 

In the corrected version, `split(', ')[1]` is added after `strip()` to extract only the version number without any additional text. This change ensures that the `info` function returns the expected output `'Fish Shell 3.5.9'`.