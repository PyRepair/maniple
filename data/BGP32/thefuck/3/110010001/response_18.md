## Analysis
1. The `Fish` class contains the `info` method that is supposed to return the name and version of the current shell (Fish).
2. The bug occurs because the function is not properly extracting the version number from the output of the command `fish -c 'echo $FISH_VERSION'`.
3. The error message highlights that the assertion failed because the expected version value is "Fish Shell 3.5.9" but the actual value extracted from the command output was "Fish Shell fish, version 3.5.9".
4. To fix the bug, we need to modify the way the version is extracted from the `Popen` process output.

## Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Correcting the way version is extracted
        version = version.split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

By splitting the version string using `', version '` as the delimiter, we extract only the version number itself, avoiding extra text like "fish, version" in the output. This modification should fix the bug and result in the correct comparison for the test case.