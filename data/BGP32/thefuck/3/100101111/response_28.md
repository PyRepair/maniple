### Analysis:
1. The `info` function is trying to retrieve the version of the Fish shell by executing a command using `Popen`.
2. The test is mocking the output of the `stdout` from the Popen call to simulate the shell version information.
3. The function currently returns the version along with extra text 'Fish Shell' which is not present in the expected output.
4. The test is expecting only the version number without the extra text.

### Bug Cause:
The bug is caused by the `info` function appending 'Fish Shell' before the actual version number, leading to a mismatch with the expected output defined in the test.

### Fix Strategy:
To fix the issue, we need to modify the return statement in the `info` function to only include the version number without 'Fish Shell'.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return version
```

By removing the extra text 'Fish Shell' from the return statement, the corrected version of the `info` function should now match the expected output in the test case and resolve the bug.