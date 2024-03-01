### Explanation:
The issue here is that the `stdout.read()` method returns a MagicMock object instead of the actual output of the command. This is causing the `version` variable to hold an incorrect value.

### Strategy for fixing the bug:
To fix this bug, we need to modify the way we read the output of the command executed by `Popen`. We should use the `communicate()` method instead of directly reading the `stdout` stream.

### Corrected version of the function:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output, _ = proc.communicate()
        version = output.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```