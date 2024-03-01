### Bug Explanation:

The buggy function `info` in the `Fish` class of the `fish.py` file is intended to return the version of the Fish Shell. However, the issue arises from the fact that the function is incorrectly formatting the version string, including unwanted characters, which causes the assertion error in the failing test.

The failing test provides a version string of `'fish, version 3.5.9'`, but the function returns `'Fish Shell fish, version 3.5.9'`. This discrepancy results in the assertion error.

The expected behavior is for the function to return `'Fish Shell 3.5.9'` after extracting and formatting the version number correctly.

### Bug Fix Strategy:

To fix the bug, we need to modify how the version string is processed in the `info` function. Specifically, we should extract the version number from the string `'fish, version 3.5.9'`, removing any unnecessary characters like `'fish, version'`. Then, we can format the extracted version number into the desired output format `'Fish Shell 3.5.9'`.

### Corrected Version:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract the version number by splitting the version string
        version_parts = version.split(', version ')
        if len(version_parts) == 2:
            version = version_parts[1]
        return u'Fish Shell {}'.format(version)
```

In the corrected version, the function splits the version string `'fish, version 3.5.9'` into parts based on the separator `', version '`. Then, it checks if there are two parts after splitting and uses the second part as the version number. This approach ensures that only the version number is included in the formatted output `'Fish Shell 3.5.9'`, resolving the bug.