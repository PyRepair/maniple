### Analysis:
The buggy function `info` is attempting to retrieve the version of the Fish shell, but it is not handling the output formatting correctly. The failing test is providing the version number in the format `'fish, version 3.5.9'`, which the function does not handle correctly.

### Bug Cause:
The bug is caused by not considering the specific output format of the `echo $FISH_VERSION` command in the Fish shell. This causes the function to include unnecessary text and commas in the output version, leading to the assertion failure in the test.

### Fix Strategy:
To fix the bug, we need to modify the way the function extracts and formats the version number from the shell command output. We should extract only the version number part of the output string and remove any unnecessary text or characters before formatting it for the return value.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip().split()[1]
    return u'Fish Shell {}'.format(version)
```

This corrected version includes additional processing on the obtained output to extract only the version number part and format it correctly for the return value. Now, the function should pass the failing test and produce the expected output.