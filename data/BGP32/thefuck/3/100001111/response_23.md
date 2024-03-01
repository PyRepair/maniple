Based on the provided information, the bug in the `info` function of the `fish.py` file is caused by returning the full version string with extra text ("Fish Shell") when the expected output only contains the version number.

To fix this bug, we should modify the function to extract just the version number from the full version string before returning it.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    
    # Extracting only the version number from the full version
    if ',' in version:  # Check if there is extra text in the version
        version_number = version.split(',')[-1].strip()  # Extract the last part as the version number
    else:
        version_number = version
    
    return version_number
```

By extracting only the version number from the full version string, we ensure that the function returns the expected output containing just the version number. This fix addresses the bug mentioned in the GitHub issue related to the recursive loop caused by the incorrect output.