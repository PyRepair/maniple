The bug in the current function is that it is checking for the presence of the word 'stash' in the second part of the split command script, which is incorrect. The correct check should be for the first part of the split script to be 'git'.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (splited_script[0] == 'git'
            and 'usage:' in command.stderr)
```

This corrected version correctly checks if the first part of the split command script is 'git' and if 'usage:' is in the command's stderr.