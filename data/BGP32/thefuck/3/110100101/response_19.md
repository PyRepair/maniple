### Analysis
The buggy function `info(self)` is attempting to retrieve the Fish shell version by running a command `echo $FISH_VERSION` using the `Popen` function. However, in the failing test case, the expected output is `'fish, version 3.5.9\n'`, but the function is attempting to extract version directly without handling the extra text. This is causing the function to return an incorrect version string.

### Bug
The bug in the current implementation is that the function does not correctly parse the output of the `echo $FISH_VERSION` command to extract only the version number. It is expecting the output to only contain the version number, but in reality, there is additional text in the output.

### Fix
To fix the bug, we need to modify the function to correctly handle and extract the version number from the output of the command. We can modify the function to split the output by spaces and extract the version number from that.

### Corrected Version
```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The corrected version of the class containing the fixed function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(' ')[-1]
        return 'Fish Shell {}'.format(version)
```

Now, the corrected function will correctly extract the version number from the output of the command, and it should pass the failing test case.