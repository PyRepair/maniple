Upon analyzing the test case and the error message, it appears that the issue lies within the `info` function of the `Fish` class. The error message indicates that the expected output is "Fish Shell 3.5.9" but the actual output is "Fish Shell fish, version 3.5.9".

The bug occurs because the `Popen` command is using the `-c` flag to execute the command specified in the string as a script using the fish shell. However, the correct command should be `fish --version` rather than `echo $FISH_VERSION`.

One possible approach to fixing the bug is to update the command passed to `Popen` to execute `fish --version` and then parse the output to extract the version number.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By using the command `fish --version` and then parsing the output to extract the version number, the bug should be resolved. This corrected code should be used as a drop-in replacement for the buggy version of the function.