### Fixing the Bug:

#### Cause of the Bug:
The bug in the `info` function is due to the incorrect parsing of the output from the `echo $FISH_VERSION` command in Fish shell. The function is expecting just the version number, but the output includes additional text `'fish, version'` which is not being handled properly.

#### Strategy for Fixing the Bug:
1. Parse the version number correctly from the output of the command.
2. Update the return statement to format the version number retrieved.

#### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_string = proc.stdout.read().decode('utf-8').strip()
    
    # Parse the version number correctly from the output
    version = version_string.split(',')[1].strip().split(' ')[1]
    
    return u'Fish Shell {}'.format(version)
```

The corrected version of the function correctly parses the version number from the output of the command and formats it accordingly. This should resolve the failing test and produce the expected output.