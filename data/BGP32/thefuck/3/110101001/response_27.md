### Analysis
The buggy function `info()` is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` and then formatting the output. However, the failing test is not passing because the expected output is `'Fish Shell 3.5.9'` while the actual output is `'Fish Shell fish, version 3.5.9'`.

### Bug
The bug in the `info()` function is that it is not correctly parsing the version from the output of the `echo $FISH_VERSION` command. It is directly using the output without extracting the version number.

### Strategy for fixing the bug
To fix the bug, we need to modify the function to extract and parse only the version number from the output of the command.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version_lines = version_output.split('\n')
        version = None
        for line in version_lines:
            if 'version' in line:
                version = line.split('version')[1].strip()
                break
        return u'Fish Shell {}'.format(version)
``` 

After applying the corrected version of the `info()` function, the failing test should now pass successfully.