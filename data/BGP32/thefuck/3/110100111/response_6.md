## Analysis
1. The `info` function in the `Fish` class is supposed to return the name and version of the current shell by executing the command `fish -c 'echo $FISH_VERSION'`. However, the output processing seems to be incorrect.
   
2. The test function `test_info` focuses on asserting that the returned string from `shell.info()` matches the expected string `'Fish Shell 3.5.9'` and also checks the command used by `Popen`.

3. From the expected values and types provided in the failing test case, it seems that the issue lies in how the output of the `Popen` process is being handled after executing the command.

4. The GitHub issue indicates a potential problem with the `thefuck` plugin in Fish Shell and how it interacts with the `thefuck` Python tool. The fix is supposed to address recursive looping caused by incorrect handling of shell version information.

## Bug Cause
- The bug in the `Fish` class's `info` function stems from the incorrect parsing of the output obtained from the `Popen` process.
- The expected output of `echo $FISH_VERSION` should be the version number only, but the current implementation is not handling this output correctly.
- This incorrect handling leads to discrepancies in the test case where the expected version number is not returned as expected.

## Fix Strategy
- We need to properly read and process the output obtained from the `proc` in the `info` function to extract the version number accurately.
- Additionally, the command being executed should match the expected command as defined in the test function.

## Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.readline().decode('utf-8').strip().split(", version ")[1]
        return f'Fish Shell {version}'
```

The corrected version includes reading the output using `proc.stdout.readline()` and then splitting the version number from the output string to extract just the version. This adjustment should ensure that the function returns the correct version number in the expected format.