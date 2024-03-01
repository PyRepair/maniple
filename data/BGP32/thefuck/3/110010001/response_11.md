### Analysis:
1. The buggy function `info` in the `Fish` class is trying to get the version of the Fish shell by executing a subprocess which runs the command `echo $FISH_VERSION`.
2. The `Popen` method is used to create a new process. However, the way the output is being read and processed is leading to the bug.
3. The error message indicates that the expected output is `'Fish Shell 3.5.9'` while the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the parsing of the version is incorrect and includes unwanted text.
   
### Bug Cause:
The bug is caused by directly using `decode('utf-8').strip()` on the output of `proc.stdout.read()`. The output is being read as raw bytes and then converted into a string, which includes the unwanted 'fish, version' part along with the actual version number.
   
### Bug Fix:
To fix the bug, we need to properly decode and parse the output of the subprocess to extract just the version number. We can achieve this by decoding the raw bytes to a string, splitting it based on the delimiter `,`, and then extracting the version number. This will ensure we get the version number without any additional text.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[-1].strip()  # Extract version number by splitting on ','
        return u'Fish Shell {}'.format(version)
``` 

After making this change, the corrected function will properly extract the version number without any additional text and pass the failing test.