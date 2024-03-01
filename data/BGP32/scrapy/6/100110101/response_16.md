### Analysis
The buggy function `convert_image` in the `images.py` file is meant to convert images to a specific format (RGB) and resize them if necessary. The bug lies in the conditional logic when handling PNG images with RGBA mode. It incorrectly converts RGBA PNG images to RGB by creating a new RGB image with a white background then pasting the original image on top. This approach results in incorrect RGB values in the converted image, leading to failing tests.

### Bug
When dealing with PNG images in RGBA mode, the function incorrectly converts them to RGB by pasting the original image on top of a white background, causing incorrect color values in the resulting image.

### Fix Strategy
To fix the bug, we should handle RGBA images differently when converting to RGB. Instead of pasting the image on a white background, we should use proper conversion techniques to maintain the color integrity during the process.

### Corrected Version

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

By modifying the conditional block for PNG images in RGBA mode to properly convert them to RGB, we ensure that the color integrity is maintained during conversion. This corrected version of the function should now pass the failing tests.