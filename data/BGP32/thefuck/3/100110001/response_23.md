The bug in the provided function `info` is due to the fact that the command `fish -c 'echo $FISH_VERSION'` is being executed to get the version of the `fish` shell but the expected output format of this command is different from the actual version number which is causing the test to fail.

To fix this issue, we need to update the command used in Popen to fetch the version number correctly. Based on the test function provided, the expected output is `fish, version 3.5.9\n` so we should modify the function to parse the output accordingly.

Here is the corrected version of the function `info`:

```python
# The corrected version of the function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Since the output is expected in the form 'fish, version x.y.z\n'
    fish_version = version.split(',')[1].split('version')[1].strip()
    
    return 'Fish Shell {}'.format(fish_version)
```

With this correction, the function now correctly extracts the version number from the command output in the expected format and should pass the failing test case.