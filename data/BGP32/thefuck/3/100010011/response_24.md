### Analysis:
The error message indicates that the `shell.info()` function is returning `Fish Shell fish, version 3.5.9` instead of `Fish Shell 3.5.9`. This discrepancy is causing the assertion error in the test case. The problem seems to be in the parsing of the output from the `fish -c 'echo $FISH_VERSION'` command.

### Bug Cause:
The issue is caused by the fact that the command `fish -c 'echo $FISH_VERSION'` is returning the text `fish, version 3.5.9\n` instead of just `3.5.9`. This text is not being parsed correctly in the function, leading to the mismatch in the expected and actual output.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the parsing of the output of the `fish -c 'echo $FISH_VERSION'` command so that only the version number is extracted without any additional text or commas.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we use the `.split(", ")` method to separate the text `fish, version` from the actual version number. This ensures that only the version number is extracted and used in the return string. Now, the function should return `Fish Shell 3.5.9` as expected.