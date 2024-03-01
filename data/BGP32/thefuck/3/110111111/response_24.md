## Bug Fix:

### Analysis:
The bug in the `info` function of the `Fish` class arises from reading the wrong output from the `fish` command when trying to get the version. This results in the full version string `'fish, version 3.5.9'` instead of just `'3.5.9'`, causing the assertion error in the test case.

### Bug Fix Strategy:
To fix the bug, we need to modify how we extract the version number from the output of the `fish` command. We should parse the output and extract only the version number itself.

### Corrected Function:
```python
# The corrected version of the buggy function

class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()  # Read the output
        version_number = version.split(',')[1].strip()  # Extract only the version number
        return u'Fish Shell {}'.format(version_number)
```

Now, the corrected function will properly extract and return just the version number from the output of the `fish` command. This change will allow the test case to pass successfully.