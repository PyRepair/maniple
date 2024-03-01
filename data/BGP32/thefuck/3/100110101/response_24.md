## Identification of the bug
1. The call to `Popen` in the `info` function is using the command `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']` as expected in the test.
2. The expected version string extracted from the output ('fish, version 3.5.9\n') is not parsed correctly.

## Bug cause
The bug is caused by the incorrect command used in the `Popen` call within the `info` function. This causes the expected version string to contain unnecessary information like 'fish, version' which is not expected by the test case.

## Strategy for fixing the bug
1. Change the command in the `Popen` call to `['fish', '--version']` to match the expected command in the test case.
2. Parse the output correctly to extract only the version number from the output string.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split()[-1]
    return f'Fish Shell {version}'
``` 

With these corrections, the function will now correctly fetch the fish version number by executing `fish --version` and parse the output to extract only the version number.