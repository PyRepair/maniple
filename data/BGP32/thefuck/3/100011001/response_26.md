### Potential Error Location
The error seems to be occurring because the `version` variable includes the extra text "fish, version" instead of just the version number. This is causing the assertion to fail.

### Bug Explanation
The bug is caused by the `shell.info()` function not correctly extracting just the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. It includes the additional text "fish, version" which is not expected.

### Bug Fix Strategy
To fix the bug, we need to modify the code to extract only the version number from the output of the command. We can achieve this by splitting the output string and extracting the version number part.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
``` 

The corrected version splits the `output` string using `', version '` as the separator and takes the second part of the split (index 1) as the version number. This should extract only the version number and fix the bug.