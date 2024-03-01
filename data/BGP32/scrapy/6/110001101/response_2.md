### Bug Explanation
The bug in the `convert_image` function arises from the incorrect condition check for PNG images with RGBA mode. The code is attempting to convert the image to RGB format, but incorrectly pastes the RGBA image onto a new RGBA background, then converts it to RGB, which leads to the conversion not being applied as expected.

### Bug Fix Strategy
To fix the bug, we need to correctly handle the conversion of PNG images with RGBA mode to RGB format by pasting the RGBA image onto an RGB background before converting it. This ensures that the conversion is applied accurately without any loss of information.

### Corrected Version of the Function
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))  # Create a new RGB background
            background.paste(image, (0, 0), mask=image.split()[3])  # Paste RGBA image onto RGB background
            image = background.convert('RGB')  # Convert the image to RGB format
        elif image.mode != 'RGB':
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

With this correction, the function correctly handles the conversion of PNG images with RGBA mode to RGB format by pasting the RGBA image onto an RGB background before converting it, ensuring that the conversion is applied accurately.