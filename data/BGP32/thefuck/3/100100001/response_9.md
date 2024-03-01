The bug in the `info` function is due to the fact that the command used to retrieve the Fish Shell version (`echo $FISH_VERSION`) is incorrect. Instead, the correct command should be `fish --version` to get the version information of the shell.

Additionally, the expected output of the command is `fish, version 3.5.9` but the function is trying to strip the output directly to obtain the version number, which will result in a wrong version. Therefore, the function needs to extract the version number correctly from the output.

Here is the corrected version of the `info` function:

```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will execute the correct command to get the Fish Shell version and then extracts the version number from the correct output format.