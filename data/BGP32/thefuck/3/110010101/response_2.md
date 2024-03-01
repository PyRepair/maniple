### Analysis
1. The buggy function `info` is supposed to return the name and version of the current shell.
2. The error message highlights the discrepancy between the expected version string ('3.5.9') and the actual version string ('fish, version 3.5.9').
3. The cause of the bug is that the `echo $FISH_VERSION` command returns the version string along with unnecessary text ('fish, version') due to the command itself.
4. To fix the bug, we need to modify the command passed to the `Popen` function to only extract the numeric version without the extra text.
5. The corrected version should extract the version string correctly and return it formatted as 'Fish Shell x.x.x'.

### Correction
```python
# The corrected version of the function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION | cut -d" " -f 3'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By adding `| cut -d" " -f 3` to the command, we extract only the third part of the output separated by spaces, which is the numeric version needed. This modification ensures that we get the correct version string without unnecessary text.