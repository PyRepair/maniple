### Analysis:
The error message indicates that the actual result from calling `shell.info()` is `'Fish Shell fish, version 3.5.9'` while the expected result is `'Fish Shell 3.5.9'`. This suggests that the version string is not correctly parsed during the execution in the `info` function.

### Error Location:
The issue is most likely in the line where the version string is read and stripped: `version = proc.stdout.read().decode('utf-8').strip()`. It seems the decoding and stripping process is not handling the output correctly.

### Cause of the Bug:
The bug is caused by how the version string is being read from the `stdout` using `proc.stdout.read().decode('utf-8').strip()`. The actual output may contain additional characters or formatting that needs to be accounted for in order to get just the version number.

### Fixing the Bug:
To fix the bug, we need to modify the parsing of the version string to extract only the version number. One way to achieve this is by splitting the result string by commas to separate the version number.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output_bytes = proc.stdout.read().strip()
    version = output_bytes.decode('utf-8').split(',')[1].strip()  # Extract version number
    return u'Fish Shell {}'.format(version)
```

In the corrected version above, we read the stdout as bytes, decode it as UTF-8, split it by commas, and strip to extract the version number. This updated approach ensures that only the version number is extracted without any additional unwanted characters.