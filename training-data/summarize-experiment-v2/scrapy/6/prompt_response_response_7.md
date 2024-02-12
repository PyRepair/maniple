The bug in the `convert_image` function is related to the conversion of image formats, resizing, and mode change. The function needs to be thoroughly reviewed and corrected to handle these operations correctly.

To fix the bug, the following changes can be implemented:
1. Add a condition to handle the case when the input image mode is 'P'.
2. Correct the resizing logic to ensure that the image is resized to the specified size.
3. Ensure that the image mode is correctly converted to 'RGB' when needed.

Here is the corrected version of the `convert_image` function:

```python
# The relative path of the buggy file: scrapy/pipelines/images.py

from PIL import Image
from cStringIO import StringIO as BytesIO
from scrapy.pipelines.images import FilesPipeline

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode == 'P':
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

With the above correction, the `convert_image` function should now correctly handle image format conversion, resizing, and mode changes, as per the requirements of the failing test cases.