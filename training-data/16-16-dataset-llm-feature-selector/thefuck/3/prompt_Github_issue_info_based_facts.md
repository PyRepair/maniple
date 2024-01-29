# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)

```

The github issue message is:
# A GitHub issue title for this bug
```text
thefuck -v hangs Fish Shell initialisation with Oh-My-Fish plugin
```

## The associated detailed issue description
```text
Oh-My-Fish's TheFuck plugin uses thefuck -v to decide when to regenerate functions. That triggers a recursive loop because of shells/fish.py:Fish.info().

Fix is on it's way.

Reference: oh-my-fish/plugin-thefuck#11
```



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


