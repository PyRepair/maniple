## Identified Bug
The bug in the `info` function of the `Fish` class is that it is not correctly extracting the version information from the output of the shell command. This causes the version information to include unwanted text like 'fish, version' which leads to the assertion error.

## Bug Cause
The bug occurs because the function is not correctly parsing the version output from the shell command. It is not considering the correct format of the output which causes the version string to include unnecessary text.

## Bug Fix Strategy
To fix the bug, we need to appropriately parse the output of the `fish -c 'echo $FISH_VERSION'` command to extract only the version number without any additional text.

## Corrected Version of the Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        bytes_version = proc.stdout.readline().strip()
        try:
            version = bytes_version.decode('utf-8').split(',')[1].strip()
        except IndexError:
            version = ''
        return u'Fish Shell {}'.format(version)
```

By modifying how the version number is extracted from the output of the shell command, the corrected function should now correctly return just the version number without any additional text. This will ensure that the function passes the failing test and provides the expected output.