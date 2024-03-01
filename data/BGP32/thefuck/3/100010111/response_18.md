### Analysis
The error message indicates that the function `info` is returning the incorrect version of the Fish shell. Instead of returning the version number only, it returns the version number along with the text "fish, version". This discrepancy causes the assertion error in the test.

The cause of this bug is that the function is not correctly parsing the output of the command `echo $FISH_VERSION` to extract just the version number.

### Fix Strategy
To fix this bug, we need to correctly extract the version number from the output of the command by removing any additional text. We can do this by splitting the output string and selecting the last part as the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    version = output.split(', version ')[1] # Extract only the version number
    return u'Fish Shell {}'.format(version)
``` 

By modifying the function to extract and return only the version number without any additional text, we can fix the bug.