### Analysis:
The error message indicates that the function `info()` in the `fish.py` file is not correctly parsing the version number of the Fish shell. The test is failing because the expected version number is not being extracted properly from the output of the command.

### Identified Issue:
The issue lies in the parsing of the version number from the output of the command `echo $FISH_VERSION`. The current implementation is reading the output without properly decoding it and extracting just the version number.

### Bug Cause:
The bug is caused by the incorrect decoding and extraction of the version number from the command output. The `strip()` method is used to remove leading/trailing whitespaces from the output, but it is not enough to extract just the version number.

### Strategy for Fixing the Bug:
1. Decode the output of the command properly to handle bytes and strings.
2. Use regex or string manipulation to extract just the version number from the output.
3. Ensure that the extracted version number matches the expected format for comparison.

### Corrected Version:
```python
import re

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    version_str = version_bytes.decode('utf-8').strip()
    version_match = re.search(r'\d+\.\d+\.\d+', version_str)
    if version_match:
        version = version_match.group()
        return u'Fish Shell {}'.format(version)
    return "Fish Shell Version Not Found"
```

### Explanation:
- The corrected version properly decodes the byte output of the command.
- It uses regular expression `'\d+\.\d+\.\d+'` to match and extract the version number from the output.
- If a match is found, it constructs the version string in the correct format.
- If no match is found, it returns a default message indicating that the version was not found.

By using this corrected version, the function should now properly extract the version number from the command output and pass the failing test case.