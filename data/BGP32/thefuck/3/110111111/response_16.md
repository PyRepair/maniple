To fix the bug in the `info` function of the `Fish` class in `fish.py`, we need to modify the command being executed to retrieve the Fish shell version. The current command `echo $FISH_VERSION` is incorrect and does not return the version in the correct format.

Based on the failing test, the expected Fish shell version is included in the output string `b'fish, version 3.5.9\n'`, and we need to extract the version number from this string.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version_info = proc.stdout.read().decode('utf-8').strip()
        version = version_info.split(' ')[-1]
        return 'Fish Shell {}'.format(version)
```

Explanation:

1. Changed the command from `echo $FISH_VERSION` to `['fish', '--version']` to get the correct version information.
2. Instead of reading the output and assuming the version is directly available, we now read the complete version information as `version_info`.
3. Split the `version_info` on space `' '` and extract the last element to get the version number.
4. Return the version number in the correct format with `"Fish Shell "` prefix.

With this correction, the `info` function should now correctly extract the Fish shell version and return it in the expected format, passing the failing test case and resolving the issue mentioned on GitHub related to incorrect Fish shell version detection.