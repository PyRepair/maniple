### Analysis:
The buggy function `info` in the `Fish` class is supposed to return the version of the Fish shell by executing a command in a subprocess. The bug seems to be related to the incorrect command being executed in the subprocess and the method of extracting the version from the output.

### Identified Issue:
1. The command `echo $FISH_VERSION` is being used in the subprocess call, but the test is actually expecting the version to be obtained from `fish --version`.
2. The decoding of the output from the subprocess may not be handled correctly, leading to unexpected behavior.

### Bug Cause:
The bug causes the test to fail because the expected output of the shell info function `Fish Shell 3.5.9` is not obtained when using `echo $FISH_VERSION`.

### Strategy for Fixing the Bug:
1. Change the command executed in the subprocess to `['fish', '--version']`.
2. Ensure proper decoding of the output from the subprocess to get the correct version information.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

With the corrected version, the `info` function in the `Fish` class should now correctly extract the version information from the Fish shell and pass the failing test.