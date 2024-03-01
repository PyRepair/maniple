### Identified Bug
The current bug in the `info` method of the `Fish` class is caused by not properly reading the version information from the output of the command `fish -c 'echo $FISH_VERSION'`. Consequently, the version string contains additional text beyond the version number, leading to a mismatch when compared with the expected output.

### Cause of the Bug
The cause of the bug lies in how the version information is extracted and formatted. The line `version = proc.stdout.read().decode('utf-8').strip()` reads the output of the process `proc` without handling the actual version string extraction correctly. As a result, the version string returned includes extra text like `'fish, version'`.

### Strategy for Fixing the Bug
To fix the bug, the version string needs to be extracted correctly from the output of the process. It seems that the output includes additional text before the version number, and we need to strip that extra text to only get the version number itself.

### Corrected Version of the Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(", version ")[1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly extract the version number from the process output and return it as expected. This should resolve the failing test and the GitHub issue related to the incorrect version information retrieval in the Fish shell.