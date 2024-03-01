### Analysis
1. The function `info` in the `Fish` class is supposed to return the name and version of the current shell (Fish shell).
2. The function uses `Popen` to run a command `fish -c 'echo $FISH_VERSION'` to get the version of the Fish shell.
3. The issue lies in reading the output of the `Popen` process and decoding it to get the version.
4. The `proc.stdout.read().decode('utf-8').strip()` method chain is incorrect and likely causing the bug.
5. We need to fix the decoding and encoding process to correctly extract the version of the Fish shell.

### Bug Explanation
The bug is caused by incorrectly reading and decoding the output of the `Popen` process. The method chain `proc.stdout.read().decode('utf-8').strip()` is not handling the decoding process properly, leading to incorrect or unexpected output.

### Fix Strategy
To fix the bug, we need to properly read and decode the output of the `Popen` process. We should decode the output using the correct encoding and handle any errors that may arise during the decoding process.

### Corrected Version
```python
# Updated version of the 'info' function in the Fish class
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    version = version_bytes.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By reading the output of the `Popen` process into `version_bytes` first, we can then decode it using the correct encoding and strip any leading or trailing whitespaces. This should fix the bug and correctly extract the version of the Fish shell.