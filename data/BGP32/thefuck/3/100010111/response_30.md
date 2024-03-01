### Analysis
The error occurred during the test of the `info()` function in `fish.py`. The test is asserting that the function should return `'Fish Shell 3.5.9'`, but the actual value returned includes the unexpected prefix `'fish, version '`.

### Identified Bug Location
The bug is in the `info()` function where the variable `version` is not correctly parsed from the output of the `Popen` process. The issue lies in how the variable `version` is being extracted after reading from `proc.stdout`.

### Cause of the Bug
The bug is caused by not correctly parsing the output from the `Popen` command. The actual value returned by the function includes the extra prefix `'fish, version '` which should be removed to match the expected value `'Fish Shell 3.5.9'`.

### Strategy for Fixing the Bug
To fix the bug, we need to extract the correct version information from the output of the `Popen` process. This can be achieved by stripping out the unwanted prefix before formatting the final output string.

### Corrected Version of the Function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    version = output.split(',')[1].strip()  # Extracting version after removing 'fish,'
    
    return u'Fish Shell {}'.format(version)
```

By splitting the `output` based on the `,` character and taking the second part, we can extract only the version number. This corrected version should now return `'Fish Shell 3.5.9'` as expected.