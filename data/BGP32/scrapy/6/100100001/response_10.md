The bug in the `convert_image` function lies in the condition checking for PNG format and RGBA mode. The code pastes the original RGBA image onto a new RGBA background instead of creating a new RGB image. This results in a mixed-mode image which causes issues when converting to JPEG format.

The bug can be fixed by creating a new RGB image when converting from PNG with RGBA mode. Here is the corrected version of the `convert_image` function:

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
    image.save(buf, 'JPEG')
    return image, buf
```

In this corrected version, we create a new RGB background image for PNG images with RGBA mode and paste the original image onto it. This ensures that the resulting image is in the correct RGB mode for saving to JPEG format.

With this correction, the `convert_image` function should pass the failing test cases provided.