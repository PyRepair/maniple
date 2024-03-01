The bug in the `info` function is caused by the fact that it is trying to extract the version information from the entire output of `echo $FISH_VERSION` command, including the unnecessary `"Fish Shell"` string. This leads to an incorrect version format which causes issues with certain plugins like Oh-My-Fish.

To fix this bug, we should modify the function to only extract the version number from the output of the command.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[-1]  # Extracting only the version number
    
    return version
```

By splitting the `version` string based on space characters and taking the last part of the split, we ensure that we only get the version number without including the unnecessary string "Fish Shell". This change should address the issue reported on GitHub and provide the correct version information for the Fish shell.