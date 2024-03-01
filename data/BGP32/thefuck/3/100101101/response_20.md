The bug in the `info` function is caused by the mismatch between the command used to retrieve the Fish shell version and the expected output compared in the test. The command `echo $FISH_VERSION` returns a string with additional information "fish, version" which is not present in the expected output.

To fix the bug, we need to update the command used to retrieve the Fish version and adjust the expected output in the test accordingly.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now correctly extract and return the Fish shell version without the additional "fish, version" text.

And here is the updated test function:

```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

By updating the `info` function to use the correct command for retrieving the Fish shell version and adjusting the expected output in the test, the corrected version should now pass the failing test.