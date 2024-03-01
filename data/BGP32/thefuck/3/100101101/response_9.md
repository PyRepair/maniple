## Bug Explanation
The bug lies in the line where the version is being extracted from the output of the command `echo $FISH_VERSION`. The expected output format is `'fish, version 3.5.9'`, but the function is only extracting the version number (`3.5.9`) without considering the prefix `'fish, version'`. This causes the mismatch in the expected and actual output values.

## Fix Strategy
To fix the bug, we need to modify the extraction of the version from the output to consider the prefix `'fish, version'`. We can do this by splitting the output string and extracting the version number part only.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1]  # Extract the version part
    return f'Fish Shell {version}'
```

By making this change, the function will correctly extract the version number from the output and format the result as expected.