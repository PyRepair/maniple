### Bug Explanation
The bug occurs when the input image has a mode of 'PNG' and 'RGBA'. In this case, the code creates a new image with a white background and pastes the original image onto it. However, the paste function was being called incorrectly causing issues with the transparency of the original image.

### Bug Fix
To fix this bug, we need to correct the way the paste function is called. By specifying the image as the first argument and not repeating it, we can ensure that the transparency of the original image is preserved when pasting it onto the white background.

### Corrected Code
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
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

By making this change in the `convert_image` function, the bug should be fixed and the failing tests should now pass.