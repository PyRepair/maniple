### Identified Bug:
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` is incorrect as it will not return the expected version information. Additionally, the test case is reading `version` using an incorrect `side_effect` value `b'fish, version 3.5.9\n'` which does not match the command output format.

### Bug Fix Strategy:
1. Modify the command used to retrieve the Fish shell version to `fish --version` instead of `echo $FISH_VERSION`.
2. Update the test case to provide the correct `side_effect` value that matches the output of the `fish --version` command.

### Corrected Version of the Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

By updating the command to `fish --version` and correctly parsing the version information, the corrected function should work as expected with the provided test case.