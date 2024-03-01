## Fixing the Bug

### Analysis
The buggy function `info` in `shells/fish.py` is trying to retrieve the Fish shell version using the command `echo $FISH_VERSION` but the test is expecting the output to be in the format `3.5.9`. This discrepancy leads to the test failing with an assertion error.

### Bug Cause
The `info` function returns the version including extra text such as `fish, version`. This additional text causes the assertion error in the test script. The output of the function should match the expected format `Fish Shell 3.5.9`.

### Strategy for Fixing
To fix this bug, we need to modify the extraction of the version from the command output to remove any additional text or formatting.

### Updated Buggy Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_extract = proc.stdout.read().decode('utf-8').strip()
    version = version_extract.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

Now, the function extracts the version number using `split(', version ')` to remove any unnecessary text and format the output correctly.

After applying this fix, the tests should pass successfully.