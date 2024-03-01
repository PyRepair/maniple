### Bug Explanation:
The bug in the `info` function of the `Fish` class arises from the fact that the `version` variable is assigned the value 'fish, version 3.5.9' instead of just '3.5.9'. This incorrect value causes the assertion error in the test because the expected output doesn't match the actual output due to the inclusion of extra text.

### Strategy for Fixing the Bug:
To fix the bug, you need to extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. This can be achieved by splitting the output string based on the comma and retrieving the second part, which corresponds to the version number.

### Corrected Version:
```python
# The relative path of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the buggy function
class Fish(Generic):
    # Corrected info function
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]
        return u'Fish Shell {}'.format(version)
```

By splitting the output based on the comma and extracting the version number, the corrected function now returns only the version number without the unnecessary text. This change ensures that the function matches the expected output and resolves the test assertion error.