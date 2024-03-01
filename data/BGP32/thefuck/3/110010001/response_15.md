## Analysis:
1. The buggy function `info` in the `Fish` class is meant to return the name and version of the Fish shell.
2. The error message indicates that the output returned by the function is in an unexpected format.
3. The error is caused due to an additional string `'fish, version'` being returned along with the actual version number.
4. To fix the bug, we need to modify the method of extracting the version number to exclude the additional string from the output.

## Bug Fix Strategy:
- Update the function to correctly split and extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.
- Modify the decoding and stripping of the output to ensure only the version number is extracted and formatted properly.

## Corrected Version: 
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output and extracting only the last element (which is the version number), we ensure that the function correctly returns the formatted version of the Fish shell without any additional unnecessary strings.