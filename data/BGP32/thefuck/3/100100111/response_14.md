## Analysis
The `info` function in the `fish.py` file is attempting to retrieve the version of the Fish Shell by executing `fish -c 'echo $FISH_VERSION'`. However, in the test file `test_fish.py`, the expected version output by the command is `fish, version 3.5.9`, whereas the function only captures `3.5.9`. This discrepancy leads to the failing test.

## Error Location
The error is in how the function reads the version from the `stdout` of the process. It assumes that only the version number will be returned, but in reality, there is extra text before the version number.

## Bug Explanation
The current implementation of the `info` function does not handle the case where additional text is included in the stdout along with the version number. As a result, the function only captures the version number and omits the text preceding it, causing the failing test.

## Bug Fix Strategy
We should modify the function to read the entire stdout message and then extract the version number from it. This way, we ensure that all the text returned by the `fish -c 'echo $FISH_VERSION'` command is considered, not just the version number.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',', 1)[-1].strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we read the entire output from the `stdout` and then extract the version number by splitting the message on commas and spaces. This ensures that we capture the version number correctly even if there is additional text in the output.