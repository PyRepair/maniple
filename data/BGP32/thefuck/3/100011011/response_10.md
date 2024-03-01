### Analysis:
The issue arises from the fact that the `info` function in the Fish shell class is returning the full output string from the command `echo $FISH_VERSION` without parsing out just the version number. This leads to a mismatch when comparing the expected version directly.

### Error Cause:
The `info` function is returning the full output string including the text "fish, version" before the actual version number. This causes the assertion error when comparing the expected output which only includes the version number.

### Fix Strategy:
Modify the function to extract only the version number from the output string before constructing the final return string.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_str = proc.stdout.read().decode('utf-8').strip()
    version = version_str.split(", version ")[-1]  # Extract just the version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the `version_str` variable and extracting only the version number, we can accurately construct the return string and pass the test.