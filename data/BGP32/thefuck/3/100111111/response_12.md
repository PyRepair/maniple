### Bug Analysis:
1. The `info` function in `shells/fish.py` is designed to return the name and version of the current Fish shell.
2. The function uses `Popen` to run the command `fish -c 'echo $FISH_VERSION'` to get the version information.
3. The failing test in `test_fish.py` sets up `Popen` to return `b'fish, version 3.5.9\n'`, but the actual output from the function includes the unnecessary `fish,` prefix.
4. The error message shows that the comparison fails due to this prefix.
5. The GitHub issue relates this problem to a recursive loop triggered by the `-v` option used in the plugin.

### Bug Location:
The bug is within the extraction of the shell version from the output obtained from `Popen`.

### Bug Cause:
The bug stems from not properly extracting the version string from the output, causing an unexpected prefix in the actual output compared to the expected one.

### Fix Strategy:
To fix the bug, we need to parse and extract the version number correctly from the output obtained from `Popen`.

### Corrected Version:

```python
def info(self):
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(", ")[-1]  # Extracting just the version part
    return u'Fish Shell {}'.format(version)
```

By splitting the output obtained from `Popen` by `", "` and taking the last part of the split, we can correctly extract the version number. This corrected version should pass the failing test and return the expected version number without the unnecessary prefix.