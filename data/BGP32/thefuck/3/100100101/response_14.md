### Analysis
1. The `Popen` function is being used to run the command `echo $FISH_VERSION` in the Fish shell and capture the output.
2. The `Popen.return_value.stdout.read()` is being used to read the output from the process.
3. The version is being extracted from the output by decoding it using utf-8 and stripping any white spaces.
4. The extracted version is then formatted as `'Fish Shell version'`.

### Bug
The bug lies in the fact that the command `echo $FISH_VERSION` is being used to extract the version, but in the test function, the expected output is `'fish, version 3.5.9\n'`. This mismatch in the expected output from the test and the actual command used to extract the version is causing the test to fail.

### Strategy for Fixing the Bug
To fix the bug, we need to update the command used to extract the version to match the expected value in the test function. We should use `fish --version` in the `Popen` command to capture the correct version information.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split()[2] if version.startswith('fish') else version
    return u'Fish Shell {}'.format(version)
```

After correction, the function should correctly extract the version from the output of `fish --version` and format it as `'Fish Shell version'`. This correction aligns the function with the expected value in the test function and ensures that the test passes successfully.