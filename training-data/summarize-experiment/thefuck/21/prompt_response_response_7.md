```python
@git_support
def match(command):
    script_words = command.script.split()
    return (len(script_words) >= 2 
            and script_words[1] == 'stash'
            and 'usage:' in command.stderr)
```