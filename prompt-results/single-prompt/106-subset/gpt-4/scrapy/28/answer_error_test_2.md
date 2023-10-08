The issue lies in the fact that the 'requests.seen' file is not getting updated whenever a request is seen. This is resulting in the `request_seen` function returning false even for requests that have been seen.

To fix this bug, we need to write to the 'requests.seen' file whenever a new fingerprint is registered. Furthermore, we need to close this file in the `close` method to avoid ResourceWarning.

Additionally, the `__init__` method tries to directly load from the unclosed file, causing inconsistent states. The fingerprints should be only loaded during the `open` method.

Here's the fixed code:

```python
import os
import logging

class RFPDupeFilter:
    def __init__(self, path=None, debug=False):
        self.file_path = None
        self.file = None
        self.fingerprints = set()
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if path:
            self.file_path = os.path.join(path, 'requests.seen')

    def open(self):
        if not self.file_path:
            return

        if os.path.exists(self.file_path):
            self.file = open(self.file_path, 'r+')
            self.fingerprints.update(x.rstrip() for x in self.file)
        else:
            self.file = open(self.file_path, 'a+')

        self.file.seek(0, os.SEEK_END)  # move file marker to the end of file.

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + '\n')  # add the new fingerprint to 'requests.seen' file.
        return False

    def close(self, reason):
        if self.file:
            self.file.close()
```

Once the rewrite is completed, all the tests should pass correctly. Also, the ResourceWarning for the unclosed file will also be handled.