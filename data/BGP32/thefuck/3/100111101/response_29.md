### Analysis:
1. The `info` function is supposed to fetch the version of the Fish shell by running a command `'echo $FISH_VERSION'` through the Popen process.
2. The test is mocking the output of the `Popen` process with the string `'fish, version 3.5.9\n'`.
3. The function then attempts to extract the version number from the output, but there is a discrepancy between the expected version number (`3.5.9`) and the extracted version number (`fish, version 3.5.9`).
4. The discrepancy seems to be due to the incorrect handling of the output string during version extraction.

### Bug:
The bug lies in the way the function attempts to extract the version number from the output of the `echo $FISH_VERSION` command. The extraction logic is not correctly parsing the output string to obtain only the version number.

### Fix:
To fix the bug, we need to update the logic for extracting the version number from the output string.
- We need to split the output string based on the delimiter `', version '`.
- We then need to extract the version number from the second part of the split string.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    # Extract version number from the output
    version = output.split(', version ')[1].strip()

    return u'Fish Shell {}'.format(version)
``` 

Now with this corrected function, the extraction of the version number will be done correctly, leading to the expected output matching the version number extracted from the output string.