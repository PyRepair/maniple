The buggy function `convert_image` has two main issues:
1. In the first if condition, the comparison of image format should be case insensitive (PNG -> png) to properly handle images in different formats.
2. In the line `background.paste(image, image)`, the second argument should be `(0, 0)` to specify the top-left corner as the starting position for pasting the image.

To fix the bug, we need to make the necessary corrections mentioned above.

Here is the corrected version of the function:

```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    def convert_image(self, image, size=None):
        if image.format.upper() == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0))
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

This corrected function will now properly handle images in different formats and paste images at the correct position on the background.