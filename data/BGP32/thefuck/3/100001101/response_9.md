### Analysis
The bug in the `info` function occurs because the `echo $FISH_VERSION` command doesn't output just the version number, but also includes additional text like "fish, version 3.5.9". This extra text causes the version variable to contain more than just the version number. The `strip()` method used to remove whitespace at the beginning and end of the string is not sufficient to extract only the version number.

### Bug in the code
The bug is caused by not properly extracting just the version number from the output of the `echo $FISH_VERSION` command.

### Fixing the bug
To fix the bug, the code needs to extract only the version number from the command output. One way to achieve this is by splitting the output based on the comma and keeping the second part containing the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

By splitting the `version_output` by `,` and extracting the second part (containing the version number), the function will now correctly return just the version number without any extra text.

This correction should now satisfy the Expected case 1 and fix the bug in the `info` function.