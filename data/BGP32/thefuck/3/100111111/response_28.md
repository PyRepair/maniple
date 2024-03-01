## Analysis
1. The `info` function in the `thefuck/shells/fish.py` file fetches the current Fish shell version by running `fish -c 'echo $FISH_VERSION'` command.
2. The failing test in `tests/shells/test_fish.py` sets up a scenario where `Popen`'s `stdout.read` method returns the string `'fish, version 3.5.9\n'`.
3. The failing test expects the `shell.info()` function to return `'Fish Shell 3.5.9'`.
4. The current code fetches the version information along with extra text leading to the test failure.

## Error Cause
The current implementation of the `info` function appends additional text to the version information obtained from the `Popen` command, causing a mismatch with the expected output according to the test.

## Bug Fix Strategy
1. Extract only the version number from the output of the `Popen` command by splitting the string.
2. Update the return statement to format the extracted version correctly.
3. Update the command in the `Popen` function to fetch only the Fish shell version directly.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
    return u'Fish Shell {}'.format(version)
```

The corrected version specifically fetches the Fish shell version from the output of the `fish --version` command and returns it as `'Fish Shell <version>'`. This modification ensures that the function returns the expected version number without additional text, resolving the test failure.