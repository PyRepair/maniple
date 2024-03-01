### Analysis
The buggy function `convert_image` is designed to convert images to RGB mode and optionally resize them. The bug occurs specifically when the input image format is 'PNG' and the mode is 'RGBA'. In this case, the function incorrectly converts the image to RGB without handling the transparency channel properly, resulting in incorrect pixel values.

### Bug Cause
The bug in the function stems from the block that converts the image to RGB when the format is 'PNG' and mode is 'RGBA'. When converting from a transparent PNG to RGB, the transparency information is lost, affecting the resulting image's colors.

### Fix Strategy
To fix the bug, we need to handle the transparency information correctly when converting from 'RGBA' to 'RGB'. One way to do this is to create a new RGBA image with a white background, composite the original RGBA image over it, and then convert the composite image to RGB.

### Fixed Version

```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255, 255))
            background = Image.alpha_composite(background, image)
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

The fixed version of the `convert_image` function now correctly handles the transparency channel when converting images from 'RGBA' to 'RGB'. It first creates a white background image with full opacity, composites the original RGBA image over it, and then converts the composite image to RGB. This ensures that transparency information is preserved during the conversion process.