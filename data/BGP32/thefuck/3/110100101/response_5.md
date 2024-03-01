## Analysis
1. The `info` function is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION`.
2. However, in the failing test, the expected version is different from the command being executed, which is `fish, version 3.5.9`.
3. The `Popen` call is using `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']` as expected in the failing test.

## Bug
The bug is in the `Popen` call inside the `info` function. It's using the wrong command (`echo $FISH_VERSION`) instead of the expected command (`fish --version`).

## Fix
To fix the bug, update the `Popen` call to use the correct command `['fish', '--version']`.

## Corrected Version
```python
# The corrected version of the buggy function

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```  

With this correction, the function should now return the correct version of the Fish shell, matching the expected value in the failing test.