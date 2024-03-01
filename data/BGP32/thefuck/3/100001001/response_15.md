### Explanation of the bug
The bug in the function lies in how the output from the `Popen` process is being handled. The `proc.stdout.read()` method returns an empty byte string because it has already been read before calling the `decode('utf-8')` method, causing `version` to be an empty string. This results in the function returning `Fish Shell ` instead of the expected version number.

### Strategy for fixing the bug
To fix the bug, we should modify how we extract the output from the `Popen` process to ensure that the output is read and decoded correctly before being used to construct the version string.

### Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    
    # Read and decode the output before using it
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    
    return u'Fish Shell {}'.format(version)
``` 

In this corrected version, we use `proc.communicate()` to read the output and then decode it to get the correct version number from the `Fish Shell` process. This modification ensures that the version string is correctly extracted and returned by the function.