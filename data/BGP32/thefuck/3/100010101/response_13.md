### Analysis
The error message indicates that the `info` function is returning the incorrect version string. It appears that the returned version includes unnecessary text `"fish, version"`. The error occurs because the function is not correctly extracting and formatting the version number.

### Bug
The bug lies in how the function is extracting the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. It is not properly handling the additional text `"fish, version"`.

### Fix
To fix the bug, we need to extract only the version number from the output and format it correctly before returning. 

### The corrected version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(" ")[-1]
    return u'Fish Shell {}'.format(version)
``` 

This corrected version reads the output from the process, extracts the version number by splitting the output by spaces and taking the last part, and then formats it appropriately before returning.