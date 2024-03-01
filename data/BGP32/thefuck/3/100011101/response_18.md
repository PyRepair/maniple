### Analysis
- The error message shows that the `info` function is returning `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`.
- The function is reading the output from the `Popen` process and including the word "fish," in the version string which is causing the mismatch.
- The expected output should only include the version number without any extra text.

### Bug Fix Strategy
- Modify the code to extract only the version number from the output string and return it with the correct format.

### Code Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

This fix modifies the version extraction step to only include the version number portion of the output, removing the additional text.