### Analysis
1. The function `info` is trying to get the version of the Fish shell by running a command in a subprocess.
2. The subprocess `Popen` is executed to capture the output, but the way the output is read and processed seems to be causing the issue.
3. The `Popen` object is used to run the command 'fish -c echo $FISH_VERSION' and capture its output. The output is then read, decoded, and stripped to get the version.
4. The bug seems to be related to how the output is processed before getting the version.

### Bug Explanation
The issue lies in how the output of the subprocess is being handled. The `proc.stdout.read()` method reads the output once, and subsequent calls will return an empty byte string. Therefore, when trying to decode and strip this empty byte string, it results in an empty version string, causing incorrect output.

### Fix
To fix the bug, we need to modify how the output is read from the subprocess. We should read the output only once and store it in a variable for decoding and stripping. 

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    proc.stdout.close()
    return u'Fish Shell {}'.format(output)
```

This corrected version ensures that the output is read and stored before decoding and stripping it, preventing the empty byte string issue. Also, it properly closes the `proc.stdout` after reading the output.