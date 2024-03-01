### Explanation:
The bug in the `info` function occurs because the command `echo $FISH_VERSION` doesn't output just the version number. Instead, it outputs "Fish version X.X.X" where X.X.X represents the actual version number. This causes the `version` variable to contain extra text that needs to be stripped out to obtain only the version number.

### Strategy for fixing the bug:
To fix the bug, we need to modify the code to extract only the version number from the output of the `echo $FISH_VERSION` command.

### The corrected version of the function:
```python
# The corrected version of the buggy file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(' ')[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By splitting the `output` of the command on whitespace and taking the last element of the resulting list, we isolate the version number from any extra text. This corrected version of the function should now return just the version number without any additional text.