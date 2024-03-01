### Bug Explanation
The bug in the `convert_image` function is in the conditional check for PNG format images with RGBA mode. When the image format is PNG and the mode is RGBA, the function attempts to convert the image to RGB format by pasting it on a new RGBA background, which results in an incorrect conversion.

### Bug Fix Strategy
To fix the bug, we need to correctly handle the conversion of PNG images with RGBA mode to RGB format without creating a new background image.

### Corrected Version of the Function
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

With this corrected version of the function, the bug related to PNG images with RGBA mode should be fixed, and the function should now handle the image format conversions correctly.