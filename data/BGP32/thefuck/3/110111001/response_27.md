### Explanation:
The buggy function `info` in the `Fish` class is not correctly fetching the version of the Fish shell. The command being used to get the version is `'echo $FISH_VERSION'`, but the test is expecting the version to be retrieved using `'fish --version'`.

### Bug:
The bug lies in the command used to fetch the Fish shell version. The function should be running `'fish --version'` instead of `'echo $FISH_VERSION'`.

### Fix:
Modify the command in the `Popen` call to `'fish --version'` to ensure the correct version is obtained.

### Corrected Version:
```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will now correctly retrieve the version of the Fish shell using the appropriate command and pass the failing test.