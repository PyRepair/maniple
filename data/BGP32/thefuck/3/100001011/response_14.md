### Analysis
The buggy function `info()` in `fish.py` is trying to retrieve the version of the Fish shell using a subprocess call. However, the test case reveals that the function is returning `'Fish Shell fish, version 3.5.9'`, which is not the expected output. The issue on GitHub indicates that this function is causing a recursive loop when the `-v` option is used with `thefuck` plugin from Oh-My-Fish.

### Identified Issue
The issue lies in the subprocess call where it executes `fish -c 'echo $FISH_VERSION'` but retrieves unexpected output `'fish, version 3.5.9'` due to potential additional unnecessary text in the version string. This discrepancy in the version string is causing problems with the Oh-My-Fish plugin.

### Fix Strategy
To resolve this issue, we should modify the subprocess call to extract only the version number without any additional text. This can be achieved by parsing the version output to extract only the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Parse and extract only the version number
    version = version.split(',')[1].strip()
    
    return u'Fish Shell {}'.format(version)
``` 

By updating the `info()` function to extract only the version number and removing any additional text, the function should now return the correct version of the Fish shell without causing issues with the Oh-My-Fish plugin.