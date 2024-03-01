## Analysis
This bug is caused by the incorrect handling of the output from the `Popen` process. The function currently reads the output using `proc.stdout.read().decode('utf-8').strip()`, but the expected output is not being parsed correctly. The error message indicates that the extracted version still contains additional information ("Fish Shell" as part of the version). 

## Bug
The bug is in how the version string is extracted and processed from the shell output.

## Fix
To fix the bug, you need to correctly parse the version number from the output of the `Popen` process. 

## Updated Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Parse the correct version by splitting the output using ', version' and keeping the second part
    version = version.split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
```

This corrected version correctly extracts the version number by splitting the output of the `fish` command and taking the second part after `', version '`. This should resolve the bug and generate the correct version string for the `info` function.