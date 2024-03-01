### Bug Analysis
The bug in the `info` function is related to how the output of the `Popen` process is being read and processed. The current implementation reads the output, which includes the text "fish, version" before the actual version number. This extra text is causing the assertion error in the test case.

### Bug Location
The bug is located in the line where the output of the `Popen` process is read:

```python
version = proc.stdout.read().decode('utf-8').strip()
```

### Cause of the Bug
The output of the `Popen` process includes the text "fish, version" before the actual version number. The code then formats this output into "Fish Shell {version}". This results in an assertion error because the expected output in the test case is "Fish Shell 3.5.9" while the actual output is "Fish Shell fish, version 3.5.9".

### Fix Strategy
We need to modify the way we read and process the output from the `Popen` process. We should extract only the version number and use it to format the output string.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    # Execute the command to get the Fish shell version
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    
    # Read the output and decode it
    output = proc.stdout.read().decode('utf-8').strip()
    
    # Extract the version number from the output
    version = output.split(' ')[-1]
    
    return u'Fish Shell {}'.format(version)
``` 

By splitting the output on empty spaces and taking the last element, we extract only the version number, which can then be used to format the desired output "Fish Shell {version}". This correction should pass the failing test case and provide the expected output.