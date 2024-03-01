## Bug Cause

The bug in the `info` function lies in the way the version information is extracted from the output of the command. The current implementation retrieves the whole line of output including "fish, version" text, resulting in an incorrect version format. This leads to the assertion error in the failing test as the expected version doesn't match the actual version.

## Fix Strategy

To fix the bug, we need to modify how the version information is extracted from the command output. Specifically, we should only extract the version number itself and exclude any additional text like "fish, version".

## Corrected Version

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extract only the version number from the output
    version = version.replace('fish, version ', '')  # Remove 'fish, version ' text
    
    return u'Fish Shell {}'.format(version)
```  

This corrected version extracts only the version number after removing the unnecessary text 'fish, version '. It should now correctly format the shell version and pass the failing test.