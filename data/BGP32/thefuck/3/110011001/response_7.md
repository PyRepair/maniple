### Analysis
1. The error message indicates that the expected output is 'Fish Shell 3.5.9' but the actual output was 'Fish Shell fish, version 3.5.9'.
2. The `Popen.return_value.stdout.read.side_effect` is set to `[b'fish, version 3.5.9\n']`, so the `proc` variable is mocked by MagicMock objects.
3. The function is fetching the value of the `FISH_VERSION` environment variable from the shell and appending it to the output message. However, the value fetched includes extra text that is not needed.
4. The bug is likely due to not parsing the fetched version correctly and including extra text in the output message.
5. To fix the bug, we need to extract and format the version number correctly before appending it to the output message.

### Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number
        version_number = version.split(',')[1].strip()
        return u'Fish Shell {}'.format(version_number)
``` 

In the fixed version, we split the `version` string using `,` as the delimiter and extract the version number from it, then format the output message with just the version number.