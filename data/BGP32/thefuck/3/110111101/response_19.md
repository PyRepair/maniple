### Bug Explanation
The bug occurs because the command used to extract the Fish version (`echo $FISH_VERSION`) does not match the actual output of the `fish --version` command, leading to a mismatch of the expected version string. Additionally, the reading and decoding of the stdout from the `Popen` process needs adjustment to extract the version accurately.

### Fix Strategy
1. Update the command in the `Popen` call to `fish --version` to match the version output correctly.
2. Adjust the process of reading and decoding stdout to extract the version string accurately.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

By making these changes, the corrected function should now correctly extract the Fish shell version and pass the failing test.