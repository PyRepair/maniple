## Analysis
1. The buggy function is `info` in the `fish.py` file, which is supposed to return the name and version of the current shell (Fish Shell).
2. The failing test asserts that `shell.info()` should return `'Fish Shell 3.5.9'`.
3. The error message indicates that the actual output includes extra text (`fish, version`) compared to the expected output.
4. The issue on GitHub suggests that the `-v` flag triggers a recursive loop issue in Fish Shell due to `thefuck` plugin.

## Error
The error exists in how the version string is extracted from the output of the Popen process. The function is not correctly parsing the version string, leading to additional text in the returned version.

## Correction Strategy
To fix the bug, we should modify the way the version string is extracted from the output. Specifically, we need to correctly extract just the version number without any additional text.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(",")[1].split()[1].strip()  # Extracting only the version number
    return u'Fish Shell {}'.format(version)
``` 

This corrected implementation should now successfully extract and return just the version number without any additional text, resolving the bug reported in the failing test.