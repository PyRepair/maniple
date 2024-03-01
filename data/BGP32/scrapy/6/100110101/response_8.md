### Bug Explanation:
The bug occurs in the `convert_image` function when handling images with transparency (mode 'RGBA'). If the image is in RGBA format and the format is 'PNG', it should convert the image to RGB format and remove the alpha channel.

The issue lies in the following lines of code:
```python
background = Image.new('RGBA', image.size, (255, 255, 255))
background.paste(image, image)
image = background.convert('RGB')
```

Here, `background.paste(image, image)` is pasting the RGBA image onto itself, which results in retaining the transparency, causing unexpected results in the converted image.

### Bug Fix Strategy:
To fix the bug, we need to create a new image as the background instead of pasting the image onto itself. Then, convert the new background image to RGB format. This will ensure that the transparency is handled correctly.

### The corrected version of the function:
```python
from PIL import Image
from io import BytesIO

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

After making these changes, the `convert_image` function should now correctly handle images with transparency (mode 'RGBA') and produce the expected output for all test cases.