### Step 1: Analyze the buggy function and error message
The `info` function is attempting to retrieve the version of the Fish shell by executing a command in a subprocess. The error message indicates that the function is returning the version along with some unnecessary text, causing the assertion to fail.

### Step 2: Identify potential error locations
1. The way the version is being extracted from the output of the subprocess might be incorrect.
2. There may be extra text being returned along with the version.

### Step 3: Explain the cause of the bug
The bug seems to be in how the version is extracted from the output of the subprocess. The function is returning the entire string `'fish, version 3.5.9'` instead of the version number `'3.5.9'`.

### Step 4: Suggest a strategy for fixing the bug
To fix the bug, we need to extract just the version number from the output of the subprocess.

### Step 5: Provide a corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version will extract the version number correctly and return it without any additional text.