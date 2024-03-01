### Explanation of the bug
The bug in the `info` function is caused by the misuse of the `proc.stdout.read()` method. The `proc.stdout.read()` method returns a `bytes` object, which is not directly decode-able using `utf-8` encoding. This results in the `.decode('utf-8')` method throwing an error and causing the function to fail.

### Bug Fix Strategy
To fix the bug, we need to properly handle decoding the bytes object returned by `proc.stdout.read()` to a string before attempting to strip it.

### Corrected Version
```python
# The relative path of the fixed file: thefuck/shells/fish.py

# The declaration of the class containing the fixed function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version_bytes = proc.stdout.read()
        version = version_bytes.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```