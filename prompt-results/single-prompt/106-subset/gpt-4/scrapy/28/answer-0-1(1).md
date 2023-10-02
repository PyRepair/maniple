The issue has occurred due to the file not being closed properly after being opened. In Python, it's always a safe practice to correctly close all resources after their usage, otherwise it may lead to unexpected behavior such as memory leak issues or hanging resources that may block other operations.

Apply the fix by using `with open()` for automatic file closure, and reposition fingerprints update operation in correctly indented place. The corrected version of the code is as follows:

```python
def __init__(self, path=None, debug=False):
    self.file = None
    self.fingerprints = set()
    self.logdupes = True
    self.debug = debug
    self.logger = logging.getLogger(__name__)
    if path:
        with open(os.path.join(path, 'requests.seen'), 'a+') as self.file:
            self.fingerprints.update(x.rstrip() for x in self.file.readlines())
```
Here self.file.readlines() will read all lines in the file and give them to the set operation. This change will make sure file is nicely closed after it's not needed. This should fix the ResourceWarning error in your test case and lets you handle the file in standard Python way that is easier to read and safer.