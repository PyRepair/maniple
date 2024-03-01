### Bug Analysis:
1. The `Popen` call in the `info` function is executing `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']`, leading to the wrong version output.
2. The test is expecting the version number to be extracted as `'3.5.9'`, but the current implementation is extracting `'fish, version 3.5.9'`. This is causing the assertion error.

### Bug Fix:
Modify the `Popen` command to execute `['fish', '--version']` to get the correct version number without additional text. Then parse the version number to format it correctly as `Fish Shell X.X.X`.

### Corrected Code:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version_number = version_output.split()[-1]
    return 'Fish Shell {}'.format(version_number)
``` 

With this corrected code, the function will return the version number without any additional text and format it correctly as `Fish Shell X.X.X`, which aligns with the expected output in the failing test.