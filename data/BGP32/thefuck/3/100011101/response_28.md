### Bug Analysis
The bug in the `info` function is causing the output to include unwanted text, leading to the assertion error in the failing test. The function is supposed to return the version number of the Fish shell using the output of the command `echo $FISH_VERSION` from the Popen process. However, the version information fetched from the process output includes additional text like "fish, version" which is not expected.

- The input parameter `version` is being extracted from the output of `proc.stdout.read()`.
- The `version` value includes additional text "fish, version" which is not part of the expected output.
- This extra text in `version` causes the assertion error when comparing the actual and expected output strings. 

### Bug Fix Strategy
To fix the bug, we need to modify how the `version` information is extracted from the process output. We should extract the actual version number string without the additional text to match the expected output format.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()  # Read the output and strip leading/trailing whitespaces
    # Extract the version number only (if it's in the format 'fish, version x.x.x')
    version = version.split(', version ')[1] if ', version ' in version else version
    return u'Fish Shell {}'.format(version)
```

By modifying the `info` function as shown above, we ensure that only the version number is included in the output without any additional text. This corrected version should now pass the failing test and return the expected output format.