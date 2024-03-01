### Analysis
The buggy function `convert_image()` in the `ImagesPipeline` class is designed to handle image conversion and thumbnail generation. It checks and converts images to the appropriate format and mode, generates thumbnails if a size is provided, and saves the image as a JPEG file in a BytesIO buffer.

The potential error locations in the function are the conditions for checking the image format and mode, the conversion process, and the thumbnail generation logic.

### Bug Explanation
1. In the first conditional block, the condition checks if the image format is 'PNG' and the mode is 'RGBA'. If both conditions are met, a new RGBA background image is created, pasted with the original image, and converted to RGB. However, the `paste()` method should take the original image as the first argument and the tuple `(0, 0)` as the second argument to position the original image at the top left corner of the background image. But here, the image is being passed twice, which causes the function to fail to execute properly for PNG images in RGBA mode.

### Bug Fix Strategy
To fix the bug, we need to correct the logic in the conditional block related to PNG images in RGBA mode. Specifically, we need to edit the `background.paste()` call to correctly position the original image on the background. Additionally, we should make sure that the image is copied before any modifications are made to prevent altering the original image.

### Corrected Version
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    def convert_image(self, image, size=None):
        if image.format and image.format.upper() == 'PNG' and image.mode == 'RGBA':
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

With this updated version, the function should now correctly handle PNG images in RGBA mode, generate thumbnails if required, and save the image as a JPEG file in a BytesIO buffer.