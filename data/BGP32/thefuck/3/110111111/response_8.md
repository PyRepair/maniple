To fix the bug in the `info` function of the `Fish` class, we need to update the command used to retrieve the Fish shell version from `$FISH_VERSION` to `fish --version` to match the expected output in the test. Additionally, we need to modify the parsing logic to extract the version number correctly.

Here is the corrected version of the `info` function:

```python
# The relative path of the corrected file: thefuck/shells/fish.py

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[1].strip().replace('version', '').strip()
        return u'Fish Shell {}'.format(version)
```

Explanation of Changes:
1. Updated the command in `Popen` to `['fish', '--version']` to match the expected output.
2. Split the version string using a comma and extracted the second part (version number).
3. Removed any unnecessary spaces and 'version' text from the version number.

With these modifications, the `info` function should now correctly extract the version number from the output of `fish --version` and return it as expected, passing the failing test scenario.