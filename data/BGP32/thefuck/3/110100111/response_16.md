## Analysis
The current `info` function in the `Fish` class is attempting to retrieve the Fish shell version using the command `echo $FISH_VERSION`, but the test is expecting the version to be extracted from `fish, version 3.5.9\n`.

Based on the provided test case, it is evident that the subprocess command used to fetch the Fish shell version is incorrect, leading to an incorrect version extraction.

## Bug Explanation
The bug arises from the incorrect subprocess command being used to fetch the Fish shell version. The `echo $FISH_VERSION` command does not provide the version in the expected format `fish, version X.X.X`. As a result, the test fails as the extracted version does not match the expected one.

## Bug Fix Strategy
To fix this bug, the subprocess command used to fetch the Fish shell version needs to be updated to `fish --version` which provides the version information in the expected format `fish, version X.X.X`.

## The corrected version of the `info` function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()  # Extract version from 'fish, version X.X.X'
    return 'Fish Shell {}'.format(version)
```

By updating the subprocess command to `fish --version` and extracting the version correctly, the corrected function now returns the expected version in the required format.