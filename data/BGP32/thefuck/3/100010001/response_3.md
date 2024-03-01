## Analysis
The `info` function is intended to retrieve the version of the Fish shell by using the `fish -c 'echo $FISH_VERSION'` command. However, the function fails to parse the output correctly, resulting in the version being displayed incorrectly.

## Potential Error Location
The error seems to be occurring due to the inconsistent output that includes the string `'fish, version'` alongside the version number. This inconsistency causes the assertion to fail as it is not matching the expected output.

## Cause of the Bug
The `info` function is attempting to create the version string by directly using the output from the `Popen` call without filtering out the extra text. This results in an incorrect version string being returned.

## Strategy for Fixing the Bug
To fix this bug, we need to update the `info` function to properly extract the version number from the command output and format it correctly before constructing the final version string. This involves splitting the output of the `Popen` call to extract only the version number part.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()  # Extract just version number
    return u'Fish Shell {}'.format(version)
```

By splitting the `output` string around the comma and taking the second part of the split (index `[1]`), we can extract just the version number without the extra text. This corrected version will return the expected version string that can pass the failing test.