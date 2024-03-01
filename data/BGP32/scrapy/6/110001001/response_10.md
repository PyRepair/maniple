### Bug Explanation

The buggy function `convert_image` has the following issues:
1. When the image format is 'PNG' and mode is 'RGBA', it attempts to create a new image with mode 'RGBA', paste the original image into it, and convert it to 'RGB'. However, the background image is created with the wrong mode (RGBA instead of RGB).
2. The function always saves the image as 'JPEG', regardless of the original format.

### Bug Fix Strategy

To fix the bug, we need to:
1. Create the background image with 'RGB' mode when converting a 'PNG' image with 'RGBA' mode.
2. Save the image in its original format instead of 'JPEG'.

### Corrected Code
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background
        
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
        
        buf = BytesIO()
        image.save(buf, image.format)
        return image, buf
```

By making these changes, the function will correctly handle different image modes and formats.