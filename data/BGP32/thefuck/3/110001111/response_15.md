The bug in the current `info` function of the `Fish` class is caused by the incorrect handling of the `Popen` object and its attributes. The issue is related to the way the `stdout.read()` method is being used to read the output from the `Popen` process. Additionally, the prefix `'Fish Shell'` is being added to the version string which results in an unintended output format.

To fix this bug, we need to correct the handling of the `Popen` object and modify the format of the version string returned.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.replace('fish, version ', '')
        return version
```

In this corrected version:
- We remove the unnecessary prefix `'Fish Shell'` from the version string.
- We correctly parse the version number by removing the `'fish, version '` prefix.
- We return only the version number without any additional formatting. 

By making these changes, the issue described in the GitHub report related to the recursive loop triggered by the `info` function should be resolved.