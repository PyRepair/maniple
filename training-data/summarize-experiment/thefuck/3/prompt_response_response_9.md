The error in the function `info` occurs because the command `fish -c 'echo $FISH_VERSION'` is used to get the version of the Fish shell, but the actual returned value includes the string "fish, version" and needs to be parsed to extract the version number.

To fix this bug, we need to modify the function to capture the correct version of the Fish shell. We can also use the `--version` flag instead of the environment variable to get the Fish shell version.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    (stdout, _) = proc.communicate()
    version = stdout.decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function now properly captures the Fish shell version and returns it as expected.

You can use this corrected code as a drop-in replacement for the buggy version of the function.