### Bug Explanation
The buggy function `convert_image` has a bug that causes it to incorrectly handle PNG RGBA images, leading to failing test cases. Specifically, when the input image is of format 'PNG' and mode 'RGBA', the function creates a new RGBA background image and pastes the original image onto it. It then converts this resulting image to RGB format. The bug lies in the line `background.paste(image, image)` where the original image is mistakenly pasted onto itself, causing unexpected behavior in the conversion process.

### Solution Strategy
To fix the bug in the `convert_image` function, we need to correctly paste the original RGBA image onto the new background image before converting it to RGB. This can be achieved by pasting the original image onto the background without triggering this bug.

### The corrected version of the function
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

After making this correction, the `convert_image` function should now properly handle PNG RGBA images without encountering the bug that caused the failing test cases.