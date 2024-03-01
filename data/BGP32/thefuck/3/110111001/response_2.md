### Explanation:
The buggy function `info` is not correctly capturing the version information from the output of the `fish` command. It is expecting the output format to be `Fish Shell 3.5.9` but the actual output is `fish, version 3.5.9`. This discrepancy in the format causes the assertion error in the test.

The mistake is in the command being executed by Popen. The correct command should be `fish --version` instead of `echo $FISH_VERSION`. This change will ensure that the output format matches the expected format for version retrieval.

### Strategy for fixing the bug:
1. Change the command in the Popen call from `echo $FISH_VERSION` to `fish --version` to get the version information in the correct format.
2. Update the way the version information is processed to strip unnecessary text and format it correctly.

### Corrected version of the function:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(", ")[1]
        return u'Fish Shell {}'.format(version)
```