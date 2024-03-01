### Bug Explanation
The bug in the `info` function is due to the way the `version` string is extracted from the output of the `fish -c 'echo $FISH_VERSION'` command. The output of the command includes both the literal string `'fish, version'` and the actual version number, which is causing the assertion to fail.

### Bug Fix Strategy
To fix this bug, we need to modify the way we extract the version number from the command output. We should only extract the version number itself, without the unnecessary additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    raw_version = proc.stdout.read().decode('utf-8').strip()
    version = raw_version.split(', version')[-1].strip()
    return u'Fish Shell {}'.format(version)
``` 

This corrected version reads the output of the command, splits it at the ', version' string, and takes the last part of the split which corresponds to the actual version number. This fix should resolve the bug and make the function return the correct version number without any additional text.