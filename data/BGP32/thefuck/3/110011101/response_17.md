### Analysis
1. The `info` function in the `Fish` class is intended to fetch the Fish shell version but is currently returning the version along with additional text that is not needed.
2. The error message indicates that the expected output is `'Fish Shell 3.5.9'` but the actual output contains extra text.
3. The current output is `'Fish Shell fish, version 3.5.9'` which includes unnecessary text before the version number.
4. To fix this bug, we need to modify the function to only extract the version number without any additional text.

### Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip() # Extracting only the version number
        return u'Fish Shell {}'.format(version)
``` 

By splitting the `version` string and extracting the actual version number, we can ensure that only the version is returned without additional text. This fix should now return `'Fish Shell 3.5.9'` as expected.