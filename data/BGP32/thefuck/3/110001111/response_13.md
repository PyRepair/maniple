Based on the provided information, the issue seems to be related to the `Fish.info()` function in the `fish.py` file of the `thefuck` project. The problem occurs when `thefuck -v` command is used with the Oh-My-Fish plugin, causing a recursive loop due to the implementation of the `Fish.info()` function.

### Potential Error Locations:
1. Reading the output from `proc.stdout` without waiting for the process to finish.
2. Parsing the `FISH_VERSION` value incorrectly.

### Cause of the Bug:
The bug is likely caused by not waiting for the `proc` process to finish before reading its output, leading to incorrect parsing of the shell version.

### Strategy for Fixing the Bug:
1. Ensure that the process is finished before reading its output.
2. Modify the parsing of the `$FISH_VERSION` variable to extract the version string correctly.

### Corrected Version of the Function:
```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        out, _ = proc.communicate()  # Wait for the process to finish
        version = out.decode('utf-8').strip()
        # Extract the version string by splitting with comma and selecting the second part
        version = version.split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

This corrected version appropriately waits for the `proc` process to finish before reading its output. It also correctly parses the version string extracted from the `$FISH_VERSION` variable based on the provided information.