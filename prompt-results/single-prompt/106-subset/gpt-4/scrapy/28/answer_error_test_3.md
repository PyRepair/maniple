You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in a comment if there exists a comment:

```python
import os

def __init__(self, path=None, debug=False):
    self.file = None
    self.fingerprints = set()
    self.logdupes = True
    self.debug = debug
    self.logger = logging.getLogger(__name__)
    if path:
        self.file = open(os.path.join(path, 'requests.seen'), 'a+')
        self.fingerprints.update(x.rstrip() for x in self.file)
```

Please find below a fixed version of the `__init__` method that ensures to close the opened file properly. I have added a `with` statement when opening the file, making sure the file is closed when the reading is done.

```python
import os

def __init__(self, path=None, debug=False):
    self.file = None
    self.fingerprints = set()
    self.logdupes = True
    self.debug = debug
    self.logger = logging.getLogger(__name__)
    if path:
        with open(os.path.join(path, 'requests.seen'), 'a+') as file:
            self.fingerprints.update(x.rstrip() for x in file)
        self.file = os.path.join(path, 'requests.seen') # Store the file path instead of the file object
```

You can use this updated version of the method to fix the bug in the python code snippet.