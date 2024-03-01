## Analyzing the buggy function

1. The `info` function in `fish.py` is supposed to return the name and version of the Fish shell by running a command and capturing the output.
2. In the failing test in `test_fish.py`, it sets up a mock `Popen` object to simulate the output of the `fish -c 'echo $FISH_VERSION'` command.
3. The expected output from the test is `'Fish Shell 3.5.9'`, but the actual output from the buggy function is incorrect.
4. The error message shows that the expected output contains the version number only, without the preceding 'fish, version'.
5. The function seems to be incorrectly parsing the output of the command and not following the expected format.

## Fixing the bug

To fix the bug, we need to correct how the function reads and processes the output of the command to extract only the version number without any extraneous text.

### Updated `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(',')[1].strip()  # Extract the version number only
    return u'Fish Shell {}'.format(version)
```

By splitting the output on the comma and taking the second part, we can extract just the version number. This fixed version of the function should now produce the correct output format expected by the test.