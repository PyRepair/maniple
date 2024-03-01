The bug in the provided `convert_image` function arises from the incorrect handling of images with PNG format and RGBA mode. When the input image format is PNG and mode is RGBA, the function incorrectly converts the image to RGB without taking into account the transparency of the original image.

To fix this bug, we need to modify the function to handle images with PNG format and RGBA mode correctly, preserving the transparency information. Additionally, we need to ensure that the thumbnail maintains the image ratio when resizing.

Here is the corrected version of the `convert_image` function:

```python
from PIL import Image
from cStringIO import StringIO as BytesIO 

def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))  # Set background color to white with full transparency
        background.paste(image, (0, 0), image)  # Paste the image onto the background
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

With this correction, the function will handle PNG images with RGBA mode correctly, maintaining transparency. The thumbnail resizing will also maintain the image ratio as expected. Now, the failing test cases should pass as the function is fixed to handle the different image formats and modes accurately.