## Analysis
- The buggy function `info` is trying to get the version of the Fish shell by running a command `echo $FISH_VERSION` using `Popen`.
- The error message indicates that the version obtained includes the text "fish, version" along with the actual version number, causing the assertion to fail.
- The expected output should be just the version number without any additional text.

## Bug
The bug is due to the incorrect handling of the output from the `Popen` command. The function is not correctly extracting only the version number from the output.

## Fix
To fix the bug, we need to modify the way the `version` variable is extracted from the output of the `Popen` command.

## The corrected version of the function
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract just the version number from the obtained output
        version = version.split(',')[1].strip().replace('version', '').strip()
        return u'Fish Shell {}'.format(version)
``` 

By splitting the output based on the comma and then extracting the version number part, we ensure that only the actual version number without any extra text is used to construct the final output string.