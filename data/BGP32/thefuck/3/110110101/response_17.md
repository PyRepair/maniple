### Analysis
- The buggy function `info` in the `Fish` class is attempting to get the version of the Fish Shell by running a command using `Popen`.
- The test is mocking the output of the command to `b'fish, version 3.5.9\n'`, which indicates that the command is returning the version string with some extra information.
- The assertion in the test fails because the actual output includes the extra information about the shell besides the version number.
- The function is reading the output without taking into account the extra information, leading to the assertion error.

### Bug Cause
The bug is due to the incorrect processing of the shell version output. The function is directly using the output string without filtering out the extra details before constructing the return string.

### Strategy for Fixing the Bug
To fix the bug:
1. Read the output string from `proc.stdout.read()` and extract only the version number.
2. Construct the return string using the extracted version number.

### Corrected Code
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version_info = proc.stdout.read().decode('utf-8').strip()
        version = version_info.split(',')[1].strip().split()[1]  # Extracting only the version number
        
        return 'Fish Shell {}'.format(version)
```

By extracting only the version number from the output, the corrected code ensures that it constructs the return string with the version number only. This change will make the function pass the test and return the expected output.