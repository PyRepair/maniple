Please fix the buggy function provided below and output a corrected version. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.


# The source code of the buggy function
```python
# The relative path of the buggy file: thefuck/shells/fish.py



    # this is the buggy function you need to fix
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
    
```


Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache
```

# The source code of the buggy function
```python
# The relative path of the buggy file: thefuck/shells/fish.py



    # this is the buggy function you need to fix
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
    
```# The declaration of the class containing the buggy function
class Fish(Generic):



# A failing test function for the buggy function
```python
# The relative path of the failing test file: tests/shells/test_fish.py

    def test_info(self, shell, Popen):
        Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
        assert shell.info() == 'Fish Shell 3.5.9'
        assert Popen.call_args[0][0] == ['fish', '--version']
```


Here is a summary of the test cases and error messages:

The failing test is associated with the `info` function in the `thefuck.shells.fish` module. The error is caused by the assertion failure within the `test_info` method of the test file `tests/shells/test_fish.py` at line 118. It seems that the expected output of `shell.info()` does not match the actual output. Specifically, the expected result is `'Fish Shell 3.5.9'`, but the actual result is `'Fish Shell fish, version 3.5.9'`. This suggests that there might be an issue with the processing of the version information in the `info` function, possibly related to the handling of the output from the Popen call.


## Summary of Runtime Variables and Types in the Buggy Function

The relevant input/output values are:
- `proc` (value: `<MagicMock name='Popen()' id='140254489932816'>`, type: `MagicMock`)
- `version` (value: `'3.5.9'`, type: `str`)

Rational: This case shows that the `proc` variable is being mocked and not actually executing the command to get the `FISH_VERSION`. This is likely the cause of the bug as it's not retrieving the correct version of the shell.


## Summary of Expected Parameters and Return Values in the Buggy Function

The function 'info' is expected to return the name and version of the current shell, "Fish Shell 3.5.9". However, the current function attempts to retrieve the version by running 'fish -c echo $FISH_VERSION' using Popen, which is not consistent with the expected behavior. The return value is based on the expectance of version directly from the Popen output, "fish, version 3.5.9". The discrepancy arises from the incorrect use of Popen and the way version is read and formatted, indicating that the function is not working as expected.


## Summary of the GitHub Issue Related to the Bug

The issue "thefuck -v hangs Fish Shell initialisation with Oh-My-Fish plugin" is caused by the recursive loop triggered by the `info` function in the `fish.py` file. When Oh-My-Fish's TheFuck plugin uses the command thefuck -v, it leads to a recursive loop due to a call to the `info` function, which causes the hang during Fish Shell initialization. This behavior has been identified as a bug, and a fix is in progress.


