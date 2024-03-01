### Analysis:
1. The `info` function in the `fish.py` file is supposed to return the name and version of the current Fish shell by running the command `echo $FISH_VERSION` using `Popen`.
2. The failing test `test_info` sets up a mock environment where the `Popen` return value for reading stdout is set to `b'fish, version 3.5.9\n'`.
3. The function is expected to extract the version number `3.5.9` from the output and format it as `'Fish Shell 3.5.9'`. However, the current implementation incorrectly formats the output including the string `'fish, version'`.
4. The `Popen` call should be `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']` as expected in the test.
   
### Bug Fix:
The key issue is the incorrect handling of the version output string from the `Popen` call. We need to modify the way the version number is extracted and formatted.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1].strip()  # Extract the version number
    return 'Fish Shell {}'.format(version)
``` 

Now, the corrected function will properly extract the version number '3.5.9' and format it as `'Fish Shell 3.5.9'`. This modification addresses the bug identified through the failing test scenario.