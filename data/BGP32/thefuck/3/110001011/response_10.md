### Potential Error Locations:
1. The Popen call with the command 'echo $FISH_VERSION' may not be capturing the correct output.
2. The decoding of the output using utf-8 may not be working as expected.
3. The strip() function used to remove leading and trailing whitespaces may not be handling the output properly.

### Cause of the Bug:
The bug seems to be related to the incorrect reading and decoding of the output from the 'echo $FISH_VERSION' command. This results in the function not returning the correct Fish Shell version.

### Strategy for Fixing the Bug:
1. Ensure that the Popen call captures the correct output.
2. Verify that the decoding using utf-8 is functioning properly.
3. Make sure that the strip() function effectively removes unnecessary whitespaces.

### Corrected Version of the Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.communicate()[0].decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

In the corrected version, the `proc.communicate()[0]` method call is used to properly read the output from the subprocess. This ensures that the correct Fish Shell version is captured and decoded. Additionally, the strip() function is applied after decoding to remove any extra whitespaces. This should resolve the issue reported in the GitHub problem.