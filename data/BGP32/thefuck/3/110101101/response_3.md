### Analysis:
1. The `info` function in the `Fish` class is supposed to return the version of the Fish shell by executing the command `fish -c 'echo $FISH_VERSION'`. 
2. The bug seems to be related to the incorrect command being used to get the Fish shell version and the way the output is being processed.
3. The test fails because the expected version is `'3.5.9'` but the function returns `'fish, version 3.5.9'`. This indicates that the function is not properly extracting the version number from the output.
4. To fix the bug, we need to modify the command to extract only the version number from the output correctly.

### Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extract only the version number
        return 'Fish Shell {}'.format(version)
``` 

By changing the command to `['fish', '--version']` and extracting only the version number, we fix the bug and ensure that the function returns the correct version format.