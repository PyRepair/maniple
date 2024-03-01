### Bug Explanation
The bug in the `convert_image` function arises from the incorrect handling of images with transparency. When the input image has a format of 'PNG' and mode 'RGBA', the function is supposed to convert it to an RGB image by pasting the RGBA image onto a white background. However, the issue lies in the line `background.paste(image, image)` where the paste method is being called incorrectly, causing the transparency channels to be ignored.

### Bug Fix Strategy
To fix the bug, we need to correctly paste the RGBA image onto the white background so that the transparency information is preserved. Additionally, we need to ensure that the image is converted to RGB when needed.

### The Corrected Function
```python
from PIL import Image
from io import BytesIO

def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
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

By correcting the paste method call and making sure that transparency information is preserved, this new function should pass the failing test cases and correctly convert images as expected.