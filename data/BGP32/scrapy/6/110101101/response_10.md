### Bug Explanation:
The bug in the `convert_image` function lies in the conditional check for PNG images with RGBA mode. The function unnecessarily creates a new image with an RGB background when the input image is in PNG format and RGBA mode. This incorrect processing results in losing transparency information.

### Bug Fix Strategy:
1. Check the image format and mode separately to handle PNG and RGBA images correctly.
2. Convert the image to RGB mode without altering the background color.

### Corrected Function:
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

After applying these fixes, the `convert_image` function should now correctly handle PNG images with RGBA mode and retain transparency information.