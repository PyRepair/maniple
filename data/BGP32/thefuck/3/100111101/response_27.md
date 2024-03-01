### Explanation:
The bug in the `info` function is due to the incorrect command used to extract the Fish shell version. The command `echo $FISH_VERSION` does not return just the version number, it returns 'fish, version x.x.x' which causes the assertion error in the test. 

### Strategy for fixing the bug:
To fix the bug, the command being run by `Popen` needs to be changed to correctly output only the version number of the Fish shell.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]
    return 'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, we will get the output 'fish, version X.X.X'. We then extract the version number using the `split` method and return it with the correct format 'Fish Shell X.X.X'. 

This corrected version should now pass the failing test.