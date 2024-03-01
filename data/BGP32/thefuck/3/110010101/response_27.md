### Explanation
The bug in the `info` function arises from reading the version output as `'fish, version 3.5.9\n'` instead of just `'3.5.9'`, causing the assertion to fail.

### Strategy for fixing the bug
To fix the bug, we need to strip the unnecessary text from the output before constructing the return message.

### The corrected version of the function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.replace('fish, version ', '')  # Strip out unnecessary text
        return u'Fish Shell {}'.format(version)
```