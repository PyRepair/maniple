The bug in the provided function `info` is due to the incorrect command used to retrieve the Fish shell version. The output of `echo $FISH_VERSION` does not provide the version in the expected format. Additionally, the test expects to compare the output against `'Fish Shell 3.5.9'`, which does not align with the actual output format.

To fix this bug, we need to update the command used to retrieve the version and modify the comparison in the test accordingly.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

With this correction, the command `'fish --version'` is used to retrieve the version, and the output is then parsed to extract the version number from the complete version string.

Now, the corrected test function should look like this:

```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

By making these changes, the function should now return the expected version string 'Fish Shell 3.5.9' and pass the failing test.