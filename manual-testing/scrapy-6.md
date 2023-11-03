

This function has a bug, can you tell me the corrected code?
Note that your should ouput full resultant function code and your changes should be as minimal as possible.

buggy code:

```python
import functools
import hashlib
import six

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from PIL import Image

from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from scrapy.http import Request
from scrapy.settings import Settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FileException, FilesPipeline

class ImagesPipeline(FilesPipeline):
    # ... other code ...

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

test code:

```python
import os
import hashlib
import random
import warnings
from tempfile import mkdtemp, TemporaryFile
from shutil import rmtree
from twisted.trial import unittest
from scrapy.item import Item, Field
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes

skip = False

try:
    from PIL import Image
except ImportError as e:
    skip = 'Missing Python Imaging Library, install https://pypi.python.org/pypi/Pillow'
else:
    encoders = set(('jpeg_encoder', 'jpeg_decoder'))
    if not encoders.issubset(set(Image.core.__dict__)):
        skip = 'Missing JPEG encoders'

def _mocked_download_func(request, info):
    response = request.meta.get('response')
    return response() if callable(response) else response

class ImagesPipelineTestCase(unittest.TestCase):
    skip = skip

    def test_convert_image(self):
        SIZE = (100, 100)
        # straigh forward case: RGB and JPEG
        COLOUR = (0, 127, 255)
        im = _create_image('JPEG', 'RGB', SIZE, COLOUR)
        converted, _ = self.pipeline.convert_image(im)
        self.assertEquals(converted.mode, 'RGB')
        self.assertEquals(converted.getcolors(), [(10000, COLOUR)])
        # check that thumbnail keep image ratio
        thumbnail, _ = self.pipeline.convert_image(converted, size=(10, 25))
        self.assertEquals(thumbnail.mode, 'RGB')
        self.assertEquals(thumbnail.size, (10, 10))
        # transparency case: RGBA and PNG
        COLOUR = (0, 127, 255, 50)
        im = _create_image('PNG', 'RGBA', SIZE, COLOUR)
        converted, _ = self.pipeline.convert_image(im)
        self.assertEquals(converted.mode, 'RGB')
        self.assertEquals(converted.getcolors(), [(10000, (205, 230, 255))])

        # transparency case with palette: P and PNG
        COLOUR = (0, 127, 255, 50)
        im = _create_image('PNG', 'RGBA', SIZE, COLOUR)
        im = im.convert('P')
        converted, _ = self.pipeline.convert_image(im)
        self.assertEquals(converted.mode, 'RGB')
        self.assertEquals(converted.getcolors(), [(10000, (205, 230, 255))])
```

error message:

```text
/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/PIL/Image.py:610: ResourceWarning: unclosed file <_io.BufferedRandom name=5>
  self.load()
/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/tests/test_pipeline_images.py:101: ResourceWarning: unclosed file <_io.BufferedRandom name=5>
  im = _create_image('PNG', 'RGBA', SIZE, COLOUR)
/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/tests/test_pipeline_images.py:102: ResourceWarning: unclosed file <_io.BufferedRandom name=6>
  im = im.convert('P')
======================================================================
FAIL: test_convert_image (tests.test_pipeline_images.ImagesPipelineTestCase)
test_convert_image
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/twisted/internet/defer.py", line 151, in maybeDeferred
    result = f(*args, **kw)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/twisted/internet/utils.py", line 221, in runWithWarningsSuppressed
    reraise(exc_info[1], exc_info[2])
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/twisted/python/compat.py", line 464, in reraise
    raise exception.with_traceback(traceback)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/twisted/internet/utils.py", line 217, in runWithWarningsSuppressed
    result = f(*a, **kw)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/tests/test_pipeline_images.py", line 105, in test_convert_image
    self.assertEquals(converted.getcolors(), [(10000, (205, 230, 255))])
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/twisted/trial/_synctest.py", line 434, in assertEqual
    super(_Assertions, self).assertEqual(first, second, msg)
  File "/usr/local/Cellar/python@3.8/3.8.18/Frameworks/Python.framework/Versions/3.8/lib/python3.8/unittest/case.py", line 912, in assertEqual
    assertion_func(first, second, msg=msg)
  File "/usr/local/Cellar/python@3.8/3.8.18/Frameworks/Python.framework/Versions/3.8/lib/python3.8/unittest/case.py", line 1118, in assertListEqual
    self.assertSequenceEqual(list1, list2, msg, seq_type=list)
  File "/usr/local/Cellar/python@3.8/3.8.18/Frameworks/Python.framework/Versions/3.8/lib/python3.8/unittest/case.py", line 1100, in assertSequenceEqual
    self.fail(msg)
  File "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/benchmarks/scrapy/6/PyRepair/benchmarks/BugsInPy_Cloned_Repos/scrapy:6/venv/lib/python3.8/site-packages/twisted/trial/_synctest.py", line 377, in fail
    raise self.failureException(msg)
twisted.trial.unittest.FailTest: Lists differ: [(10000, (0, 127, 255))] != [(10000, (205, 230, 255))]

First differing element 0:
(10000, (0, 127, 255))
(10000, (205, 230, 255))

- [(10000, (0, 127, 255))]
?             -----

+ [(10000, (205, 230, 255))]
?           +++++++


----------------------------------------------------------------------
Ran 1 test in 0.049s
```
