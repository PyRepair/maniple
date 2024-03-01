### Analysis
1. The buggy function `info` is trying to retrieve the version of the Fish shell by executing a command using `Popen`. 
2. The error message shows that the version retrieved includes extra characters `fish,` which causes the assertion failure.
3. The bug is caused because the command in `Popen` includes `echo $FISH_VERSION`, which is returning `fish, version 3.5.9\n` instead of just the version number.
4. To fix the bug, we need to modify the command passed to `Popen` to only retrieve the version number without any extra characters.
5. We need to extract just the numerical version from the output of the command executed.

### Bug Fix
```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION | cut -d " " -f 3'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

With this fix, we are modifying the command passed to `Popen` to include a `cut` command that will extract the third field (which is the version number) from the output of `echo $FISH_VERSION`. This will ensure that only the version number without any extra characters is retrieved and returned by the `info` function.