The bug in the provided function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is incorrect, it should be `fish --version` to correctly capture the shell version.

Here is the corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extracting the version number
    return u'Fish Shell {}'.format(version)
```

By using the correct command to retrieve the shell version (`fish --version`), the function will now correctly extract and return the version number. This fix should make the failing test pass as it now aligns with the expected output.