## Analysis
The `info` function is attempting to retrieve the version of the Fish shell by running `echo $FISH_VERSION` command using `Popen` and then reading the output. However, the issue arises because it includes the actual shell name ("Fish Shell") in the returned version string. The issue causes a problem for another plugin that uses the returned version.

## Bug Cause
The bug causes the version string to include "Fish Shell", causing issues with the Oh-My-Fish plugin that triggers a recursive loop.

## Fix Strategy
We need to modify the function to only include the version number without the extra text "Fish Shell".

## Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extracting only version number
    version = version.replace("fish, version", "").strip()
    
    return version
``` 

With this corrected version, the function will only return the version number without any additional text, satisfying the expected output and resolving the issue described in the GitHub post.