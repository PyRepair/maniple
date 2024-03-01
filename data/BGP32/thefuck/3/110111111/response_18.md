To fix the bug in the `info` function of the `Fish` class, we need to modify the command used to fetch the Fish shell version. The command being used in the buggy function is `echo $FISH_VERSION`, which returns a string containing additional information along with the version number. We need to extract only the version number from this string.

Here's the corrected version of the `info` function:

```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_info = proc.stdout.read().decode('utf-8').strip()
        version = version_info.split(", version ")[1]
        return u'Fish Shell {}'.format(version)
```

Explanation:
- In the corrected version, `version_info` contains the entire output of the command.
- By splitting `version_info` using `", version "` as the separator, we extract the version number part.
- This version number is then used to format the return value of the function.

This corrected version will now properly extract the version number from the Fish shell output and return it in the correct format, passing the failing test case and addressing the issue reported on GitHub related to Fish Shell initialization with the Oh-My-Fish plugin.