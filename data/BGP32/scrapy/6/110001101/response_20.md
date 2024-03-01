### Bug Explanation:
The bug in the `convert_image` function arises from the incorrect condition checking for PNG images with RGBA mode. The condition `if image.format == 'PNG' and image.mode == 'RGBA':` is not accurate because the image format is not necessarily directly linked to the image mode. This leads to the incorrect handling of PNG images with RGBA mode.

### Fix Strategy:
1. Change the condition to specifically check for the image mode as RGBA for PNG images.
2. Create a new background image with RGB mode and paste the original image on it before converting it to RGB.

### Corrected Function:
```python
from PIL import Image
from cStringIO import StringIO as BytesIO
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """
    
    def convert_image(self, image, size=None):
        if image.format.upper() == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
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