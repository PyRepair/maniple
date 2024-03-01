### Analysis
1. The `info` function in the `Fish` class is trying to retrieve the version of the Fish shell by executing a command `echo $FISH_VERSION`.
2. The expected version format is `3.5.9` but the command output is in the format `fish, version 3.5.9`.
3. The error message points out the mismatch between the expected and actual versions.
4. The issue lies in how the version is being extracted from the command output.
5. We should parse the version correctly from the command output to match the expected format.

### Bug Fix Strategy
To fix the bug:
1. Update the command in `Popen` to `fish --version` to get the version in the correct format.
2. Parse the version correctly from the command output to extract just the version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version_raw = proc.stdout.read().decode('utf-8').strip()
        version = version_raw.split()[-1].replace('v', '')  # Extract just the version number
        return u'Fish Shell {}'.format(version)
```

The corrected version fixes the bug by using `fish --version` command and correctly extracting the version number, addressing the mismatch issue.