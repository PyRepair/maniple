### Bug Explanation
The buggy function is attempting to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` using the subprocess module. It reads the output of the command and expects it to be of the form `fish, version x.x.x` where `x.x.x` is the version number. However, the function is not correctly handling the output format of the command, leading to the version string being `'fish, version 3.5.9'` instead of just `'3.5.9'`.

### Bug Fix Strategy
To fix the bug, we need to modify the way the version string is extracted from the output of the subprocess command. We should only extract the version number (e.g., `3.5.9`) and not include any additional text like `'fish, version'`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_with_prefix = proc.stdout.read().decode('utf-8').strip()
    version = version_with_prefix.split(' ')[-1]
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version, we first extract the whole output string from the command, then split it by space and take the last element as the version number. This ensures that only the version number (e.g., `3.5.9`) is included in the final output.