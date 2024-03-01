Based on the provided information, the bug in the `info` function of the `Fish` class seems to be related to reading the version of Fish shell incorrectly. The incorrect version output causes the test to fail. Below is the corrected version of the function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(' ')[-1]  # Extract the version number from the output
        return 'Fish Shell {}'.format(version)
```

Explanation:
- The original code was calling `fish -c 'echo $FISH_VERSION'` to get the version, which was incorrect. Instead, we should use `fish -v` to fetch the version information.
- The `split(' ')` and `-1` usage allows extracting only the version number from the output.
- By making these changes, the corrected function should now return the correct version of the Fish shell.

By implementing this fix, the test case provided should pass successfully.