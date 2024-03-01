## Analysis
The buggy function `info` is attempting to get the version of the Fish Shell by executing a command and reading the output. However, the issue lies in the fact that the command `echo $FISH_VERSION` is actually returning a string that includes extra information (`fish, version 3.5.9`), resulting in the version string extracted to be inaccurate.

The failing test is expecting the version string `'3.5.9'` but getting `'fish, version 3.5.9'` which causes the assertion error.

## Bug Cause
The bug is caused by the incorrect command used to fetch the Fish Shell version from the environment. The command `echo $FISH_VERSION` results in additional text being included in the output along with the version number.

## Fix Strategy
To fix the bug, we need to modify the command that is being executed to ensure that only the version number is extracted without any additional text. This can be achieved by parsing the output string to extract only the version number before returning it as part of the shell info.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_with_text = proc.stdout.read().decode('utf-8').strip()
    
    # Extracting only the version number from the output
    version = version_with_text.split(' ')[-1]
    
    return u'Fish Shell {}'.format(version)
```

By splitting the output string and extracting the last element (which is the version number), we ensure that only the version number is returned without any additional information. This corrected version should now pass the failing test and provide the correct output.