### Analysis
The bug in the function is causing the version string to include unnecessary text ("fish, version"). This extra text is causing the assertion error in the test, as the expected output is just the version number without any additional text.

### Bug Cause
The bug is caused by the line `version = proc.stdout.read().decode('utf-8').strip()` where it reads the output of the process and includes the "fish, version" text in the version variable.

### Fix Strategy
To fix the bug, we need to extract only the version number from the output string without the extra text. This can be achieved by splitting the output string and extracting the version number.

### The Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()  # Extract version number
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output string at the comma and keeping only the second part (the version number), we can ensure that the function returns the correct output without the unnecessary text. This corrected version should pass the failing test.