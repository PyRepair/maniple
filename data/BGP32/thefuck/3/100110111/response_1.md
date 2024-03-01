### Analysis
1. The `info` function in the `fish.py` file is supposed to retrieve the version of the Fish shell by executing the command `echo $FISH_VERSION`. The test case fails with an assertion error because the returned version string includes additional characters.
2. The root cause of the bug seems to be the parsing of the output of the command `echo $FISH_VERSION`.
3. The failing test case expects the version to be `3.5.9` but receives `fish, version 3.5.9`.

### Bug Cause
The bug is caused by the incorrect parsing of the version string retrieved from the Fish shell. The extra characters `fish, version` are not part of the actual version, leading to the assertion error.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the parsing logic to extract only the version number from the output obtained from `echo $FISH_VERSION`.

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Split the output by ',' and extract the version part
    version_str = version.split(',')[-1].strip()
    return u'Fish Shell {}'.format(version_str)
```

By splitting the `version` string obtained from the output of the command and extracting the version part only, we ensure that the returned version matches the expected value in the test case.

This corrected version of the function should pass the failing test case and provide the expected output.