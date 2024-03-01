The bug in the provided function is due to the incorrect command used to get the Fish shell version. The function is using 'echo $FISH_VERSION' command, but the expected command should be 'fish --version'.

### Error:
The function is not executing the correct command to get the Fish shell version, leading to the version not being extracted correctly.

### Fix:
Modify the command executed by Popen to 'fish --version' instead of 'echo $FISH_VERSION'.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By making this change, the function should now correctly extract the Fish shell version and pass the failing test.