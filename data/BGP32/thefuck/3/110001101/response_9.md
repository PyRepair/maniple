### Bug explanation
The bug in the provided function is caused by the incorrect handling of the output obtained from the Popen process. The `proc.stdout.read()` call returns a bytestring, not a regular string. This bytestring needs to be decoded to a regular string using the `decode('utf-8')` method before it can be stripped and used in the final output.

### Bug fix strategy
To fix the bug, we need to modify the line `version = proc.stdout.read().decode('utf-8').strip()` by adding the `decode('utf-8')` method to properly decode the bytestring output.

### Corrected version of the function
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```