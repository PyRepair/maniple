### Analysis:
The buggy function `convert_image` is expected to handle different image formats and modes, converting them to RGB mode and resizing them if a size parameter is provided. However, the function has a bug related to handling PNG images with RGBA mode. When the input image is PNG with RGBA mode, the function is creating a new background image with RGBA mode and then converting it to RGB mode, which leads to unexpected behavior.

### Bug:
The bug lies in the code block that handles PNG images with RGBA mode. Instead of creating a new background image with RGBA mode and then converting it to RGB mode, we should directly convert the input image to RGB mode.

### Fix:
To fix the bug, we need to adjust the code block that handles PNG images with RGBA mode. We should directly convert the input image to RGB mode without creating a new background image.

### Corrected Version:
```python
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