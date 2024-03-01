### Bug Explanation:
The bug in the `info` function of the `Fish` class in `fish.py` is caused by not properly reading the output from the subprocess `Popen` when trying to get the version of the Fish shell. The current implementation does not correctly decode the output from the subprocess, resulting in an incorrect version string being returned.

When the test case is run, it expects the version string to be 'Fish Shell 3.5.9', but the actual value obtained from the subprocess is 'fish, version 3.5.9'. This discrepancy in the version string causes the assertion error.

### Fix Strategy:
To fix this bug, the output from `proc.stdout.read()` needs to be properly decoded and formatted to extract the correct version string. Additionally, the version format should match what the test case expects.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip() # Extract the version from the output
        return u'Fish Shell {}'.format(version)
```

By splitting the decoded output using ',' and taking the second part to extract the version, we can fix the bug and ensure that the correct version string is returned. This correction should resolve the failing test case and address the issue reported on GitHub.