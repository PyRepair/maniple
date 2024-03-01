### Bug Explanation

The bug in the `convert_image` function occurs due to the incorrect handling of images with transparency. When the input image format is PNG and its mode is RGBA, the function attempts to convert it to RGB by creating a new RGBA background and pasting the original image on it. However, the paste operation is incorrect, resulting in the loss of transparency information.

### Bug Fix Strategy

To fix the bug, we need to ensure that the transparency information is preserved when converting RGBA images to RGB. One way to achieve this is using the `Image.alpha_composite` function to merge the original image with a white background while preserving the transparency.

### Corrected Function
```python
from PIL import Image
from PIL import ImageOps
from cStringIO import StringIO as BytesIO

class Pipeline:
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255, 255))
            image = Image.alpha_composite(background, image).convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

By using `Image.alpha_composite` to merge the RGBA image with a white RGBA background before converting it to RGB, we can preserve the transparency information. This corrected function should now pass all the test cases provided.