The bug in the provided function lies in the way it retrieves the version of the Fish shell. The function attempts to extract the version by running the command "echo $FISH_VERSION", but the failing test expects it to run "fish --version". This mismatch in the expected command is causing the test to fail.

To fix this bug, we need to update the command executed by Popen to retrieve the shell version. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function now runs the correct command "fish --version" to obtain the version of the Fish shell, which matches the expectation in the failing test.