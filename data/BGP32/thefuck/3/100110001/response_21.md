### Analysis:
- The `info` function in the `fish.py` file is supposed to return the version of the Fish shell. However, it is not fetching the correct output from the command executed.
- The test is mocking the output of the command `echo $FISH_VERSION` as `b'fish, version 3.5.9\n` but the function is trying to format this output directly with 'Fish Shell'.
- The expected output is `Fish Shell 3.5.9` but the actual output is `Fish Shell fish, version 3.5.9`.

### Strategy for Fixing the Bug:
- Update the command being passed to Popen to fetch just the version number without any additional text.
- Strip out any additional text and commas from the version number before formatting it.

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    raw_output = proc.stdout.read().decode('utf-8').strip()
    version = raw_output.split(', version ')[-1].replace('\n', '')
    return u'Fish Shell {}'.format(version)
``` 

This corrected version uses the `--version` flag to get just the version number and then processes the output to extract and format the version number correctly.