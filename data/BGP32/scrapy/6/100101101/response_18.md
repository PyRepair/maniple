### Bug Analysis
The buggy function `convert_image` has multiple issues:
1. In the condition where `image.format == 'PNG' and image.mode == 'RGBA'`, the image is converted to RGB but using a wrong background image. The correct background should be a solid white image not the original image itself.
2. When resizing the image, the function saves the image in JPEG format regardless of the original image format. This can cause issues especially when dealing with transparent images.
3. In some cases, the function does not handle the transparency of images correctly.

### Bug Fix Strategy
1. Use a solid white background image when converting RGBA PNG images to RGB.
2. Save the converted image in the original image format to maintain image integrity.
3. Ensure transparency is handled correctly when converting images.

### Corrected Version of the Function
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, format=image.format)
    return image, buf
```

By making the above corrections, the function should now handle different image formats and modes correctly, including transparent images, and save the converted image in the original format.