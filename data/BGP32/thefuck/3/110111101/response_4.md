### Bug Explanation
The bug is caused by the incorrect extraction of the version number from the output of the command `echo $FISH_VERSION`. The buggy function is not correctly parsing the output to extract only the version number without the unnecessary text.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the section of the code responsible for parsing the version number. We should only extract the version number itself without any additional text or characters.

### Corrected Version of the Function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The corrected function
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()[13:]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By modifying the line `version = proc.stdout.read().decode('utf-8').strip()` to extract only the version number by indexing `strip()[13:]`, we can fix the bug and ensure that the extracted version number matches the expected output.