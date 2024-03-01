## Bug Explanation
The bug in the `info` function of the `Fish` class arises from the fact that the variable `version` extracted from the output of the `fish -c 'echo $FISH_VERSION'` command includes extra text, "fish, version", which is not supposed to be part of the version number. This extra text causes the assertion error when comparing the output with the expected value.

## Fix Strategy
To fix the bug, we need to extract only the version number from the `proc.stdout` output by splitting the string and keeping only the version part without the extra text. This will ensure that the extracted version matches the expected output.

## Corrected Version
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(",")[1].strip()
    return u'Fish Shell {}'.format(version)
```

By splitting the string on the comma and keeping the second part, we extract only the version number without the extra text. This should resolve the bug and make the function return the correct version number for comparison.