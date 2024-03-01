### Analysis
1. The `info` function in the `fish.py` module is supposed to retrieve the version of the Fish shell by executing `echo $FISH_VERSION` in a subprocess. However, it currently attempts to read the output of this subprocess but does not properly handle the output format.
2. The failing test sets the expected output to `'Fish Shell 3.5.9'` but the function returns a string with the pattern `'Fish Shell <version>'`.
3. The function is not correctly parsing the version string obtained from the subprocess, leading to a mismatch with the expected output in the test.

### Bug Cause
- The `info` function is not correctly extracting the version number from the output of the subprocess.
- The version string extracted is not in the expected format leading to the assertion error in the test.

### Fix Strategy
- Modify the function to correctly extract and format the version number from the output.
- Adjust the `assert` statement in the test to match the expected output format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract version number from the formatted string
    if ',' in version:
        version = version.split(',')[1].strip()
        
    return u'Fish Shell {}'.format(version)
``` 

After making this correction, the `info` function should be able to correctly extract the version number and format it as expected. The failing test should pass with the updated function.