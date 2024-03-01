### Bug Explanation
The bug in the `info` function is caused by incorrectly extracting the version information from the output of the subprocess. The function is currently extracting the version directly without filtering out any extra information such as "fish, version" before the actual version number.

### Fixing the Bug
To fix the bug, we need to modify the extraction logic to only retrieve the version number without any additional text. We can achieve this by splitting the output string based on a separator ("," in this case) and then selecting the second part, which should be the actual version number.

### Corrected Version
```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[-1].strip()  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```