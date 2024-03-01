## Analysis:
- The buggy function `convert_image` is intended to handle image conversion and resizing operations.
- The function checks the image format and mode and performs conversions accordingly.
- There are potential error locations in the conditional statements where image format and mode are checked.
- The bug seems to be related to the condition for handling PNG images with RGBA mode.

## Bug Cause:
- The bug is likely caused by the condition `if image.format == 'PNG' and image.mode == 'RGBA'`.
- In the failing test case, when converting a PNG image with RGBA mode to JPEG, the function incorrectly creates a white background with an RGBA mode instead of an RGB mode.
- This leads to an incorrect conversion and fails the test asserting that the converted image mode should be RGB.

## Fix Strategy:
- Update the condition for handling PNG images with RGBA mode to properly convert them to RGB mode without introducing unnecessary background operations.
- Ensure that the conversion logic covers all possible image format and mode combinations.

## Corrected Version:
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By updating the condition handling PNG images with RGBA mode and converting them directly to RGB mode, the corrected function should now pass the failing test case successfully.