## Analysis
- The buggy function `info` is trying to retrieve the version of the Fish shell using a subprocess call to `fish -c 'echo $FISH_VERSION'` and then formatting the output into a string. 
- The error message shows that the assertion fails because the actual output includes extra text that is not present in the expected output.
- The expected output is `'Fish Shell 3.5.9'`, while the actual output is `'Fish Shell fish, version 3.5.9'`.
- This discrepancy is likely due to the way the version string is being retrieved and parsed from the subprocess output.

## Bug
The bug in the function is caused by including the unnecessary text "fish, version" in the returned version string. This extra text is not part of the version number itself and causes the assertion failure.

## Fix
1. Modify the function to extract only the version number from the output of the subprocess command.
2. Update the format of the returned string to include `'Fish Shell'` followed by the retrieved version number without any additional text.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output at the comma and selecting the second part, we extract only the version number without any additional text. This corrected version should now pass the failing test and provide the expected output.