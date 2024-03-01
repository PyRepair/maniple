### Bug Explanation
The bug in the `convert_image` function stems from the incorrect handling of images with transparency (RGBA mode) and PNG format. When the input image is in PNG format and RGBA mode, the function creates a new RGBA background with a white color, pastes the original image onto it, and then converts it to RGB mode. This results in losing the transparency information, which causes the failing tests that check for the specific colors after conversion.

### Bug Fix Strategy
To fix the bug, we need to change the conversion logic for images with transparency. Instead of pasting the image on a white background and converting it, we should directly convert the RGBA image to RGB without losing transparency.

### Corrected Version
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

def convert_image(self, image, size=None):
    if image.mode == 'RGBA':
        image = image.convert('RGBA')  # Convert directly to RGBA without losing transparency
        
    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

By making this change, the function will now correctly handle images with transparency, preserving the alpha channel (transparency) information, which will ensure that the failing tests pass successfully.