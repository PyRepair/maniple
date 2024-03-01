### Analysis
1. The buggy function `info` is supposed to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected version value is `'3.5.9'`, but the actual value contains extra information `'fish, version 3.5.9'`.
2. The cause of this discrepancy is the incorrect command being used to retrieve the version in the `info` function. Additionally, the decoding and stripping of the output are not handled correctly.

### Bug Fix Strategy
To fix this bug, we need to modify the command in the `Popen` call to directly invoke `fish --version` to retrieve the correct version information. We also need to handle the decoding and stripping of the output properly.

### Corrected Code
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

By using `fish --version` directly, we can ensure that only the version information is retrieved. Additionally, the decoded output is split by `,` to extract the version string accurately.