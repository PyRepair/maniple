### Analysis
1. The error message indicates that the function is returning the version of Fish shell along with unnecessary text. This causes the assertion to fail.
2. The `version` variable is being set to the output of `proc.stdout.read().decode('utf-8').strip()`, which is causing the additional text to be included in the final output.
3. The expected output should be just the version number without any additional text.
4. To fix the bug, we need to modify the `version` variable to extract only the version number from the output.
5. We can achieve this by splitting the output string by comma and extracting the second part, which contains the version number.

### Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```  