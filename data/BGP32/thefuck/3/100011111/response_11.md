### Analysis
The buggy function `info` is supposed to return the name and version of the current shell, in this case, the Fish Shell version. The bug is causing the function to return the version with additional text "fish, version" which is not expected. The error message shows the actual output and the expected output for the version number. The issue on GitHub explains that this bug causes a recursive loop when using the `-v` flag with TheFuck plugin in Oh-My-Fish.

### Bug Cause
The bug is caused by the `info` function not correctly parsing the Fish Shell version output and returning it with the extra text. The `fish` command is being called with the `-c` flag to execute the `echo $FISH_VERSION` command and then the version is read from the output. The bug is likely due to the incorrect parsing of the version string from the output.

### Fix Strategy
To fix the bug, we need to modify the way the version string is extracted from the output of the `fish -c` command. We should extract only the version number without any additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number from the output
    version = version.split(', version ')[1] if ', version ' in version else version
    return u'Fish Shell {}'.format(version)
``` 

This corrected version of the `info` function should now correctly extract and return the Fish Shell version without any additional text.