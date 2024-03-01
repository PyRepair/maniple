### Bug Explanation
The bug in the `info` function lies in how the output of the `Popen` process is being read. The `proc.stdout.read().decode('utf-8').strip()` method is causing issues with not properly reading the output.

### Fix Strategy
To fix this bug, it is better to use `communicate()` method on the `Popen` object to properly read the output of the process.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

After making this change, the function should be able to correctly read the output of the `Popen` process and return the expected result.