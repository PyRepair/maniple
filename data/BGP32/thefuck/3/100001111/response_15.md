The bug in the `info` function is caused by the process hanging due to a recursive loop triggered by the use of `thefuck -v` in the context of Oh-My-Fish plugin. The recursive loop occurs because the function is attempting to get the Fish shell version using `echo $FISH_VERSION` but the output includes additional information such as the shell name 'fish, version 3.5.9' instead of just the version number.

To fix this bug, we need to modify the function to only extract the version number without the shell name. 

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION | sed "s/fish, version //"'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By adding `| sed "s/fish, version //"` to the command used by Popen, we are using the `sed` command to remove the 'fish, version ' prefix from the output, leaving only the version number.

This correction ensures that only the version number is extracted, resolving the recursive loop issue and the hanging problem, as reported in the GitHub issue.