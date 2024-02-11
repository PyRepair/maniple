Buggy function:
```python
# The relative path of the buggy file: thefuck/shells/fish.py

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

Fix for the failing test case:
```python
# The relative path of the failing test file: tests/shells/test_fish.py

def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.return_value = b'fish, version 3.5.9\n'
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

After fixing the buggy function and the failing test, the issue reported on GitHub will also be resolved.