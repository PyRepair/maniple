Your task is to assist a developer in analyzing a GitHub issue to identify a bug in a program. You will receive the source code of the function suspected to contain the bug, along with associated GitHub issue. Your role is not to fix the bug but to summarize how the function implementation contributes to the faulty behaviour described in the issue. You summary needs to be a single paragraph; it must refer to concrete details from the issue description.

# The source code of the buggy function
```python
# The relative path of the buggy file: thefuck/shells/fish.py



    # this is the buggy function you need to fix
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
    
```

# A GitHub issue for this bug

The issue's title:
```text
thefuck -v hangs Fish Shell initialisation with Oh-My-Fish plugin
```

The issue's detailed description:
```text
Oh-My-Fish's TheFuck plugin uses thefuck -v to decide when to regenerate functions. That triggers a recursive loop because of shells/fish.py:Fish.info().

Fix is on it's way.

Reference: oh-my-fish/plugin-thefuck#11
```