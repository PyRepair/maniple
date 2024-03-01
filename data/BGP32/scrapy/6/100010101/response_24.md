### Analysis
The buggy function `convert_image` is designed to convert images to RGB format and resize them if needed. However, there are several issues in the logic of the function:
1. When dealing with PNG images in RGBA mode, the background is created for conversion but the paste operation is incorrectly performed. This leads to incorrect conversion results.
2. In the case of images with modes other than RGB, the conditional check does not handle them properly.

### Bug Cause
The bug causes incorrect image conversion and resizing due to incorrect image manipulation operations for PNG RGBA images. Additionally, images with modes other than RGB are not properly handled for conversion.

### Fix Strategy
1. Correct the operation for pasting the image onto the background in the case of PNG RGBA images.
2. Add a conditional check to properly handle images with modes other than RGB for conversion.

### Corrected Version

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```