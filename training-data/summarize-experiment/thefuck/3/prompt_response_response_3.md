The error message indicates that the expected output is 'Fish Shell 3.5.9' while the actual output is 'Fish Shell fish, version 3.5.9'. This indicates that the `info` function is not correctly parsing the version number from the shell command output.

Upon analyzing the variable runtime values, it can be seen that the `proc.stdout.read` is a MagicMock object instead of the actual output of the command. This is likely the cause of the incorrect behavior in the `info` function.

To fix the bug, the function needs to correctly capture the output of the command and parse the version number from it. The `Popen` command should be used to capture the correct output from the shell command. Additionally, the string manipulation to extract the version number from the output needs to be adjusted.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.communicate()[0].decode('utf-8').strip().split()[-1]
    return 'Fish Shell {}'.format(version)
```

This revised function uses `proc.communicate()[0]` to capture the correct output of the shell command, and then manipulates the output to extract the version number. This should resolve the issue and produce the expected output 'Fish Shell 3.5.9'.