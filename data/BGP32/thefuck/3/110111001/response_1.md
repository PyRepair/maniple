### Bug Analysis
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell using the command `echo $FISH_VERSION`. However, the test is expecting the output in the format `3.5.9`, whereas the current implementation returns the version along with additional text `fish, version`.

### Bug Explanation
The test is failing because the expected output `'Fish Shell 3.5.9'` does not match the actual output `'Fish Shell fish, version 3.5.9'`. This discrepancy is due to the additional text `"fish, version"` included in the returned version value.

### Bug Fix Strategy
To fix this bug, we need to modify the `info` function to extract only the version number from the output of the `echo $FISH_VERSION` command.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(', version ')[-1]  # Extract only the version number
        return f'Fish Shell {version}'
``` 

With this correction, the function `info` will extract the version number from the output and return it in the format expected by the test.