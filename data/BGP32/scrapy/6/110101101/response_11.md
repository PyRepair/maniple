### Explanation:
The bug in the `convert_image` function is in the conditional statement checking for PNG format and RGBA mode. When an image has PNG format and RGBA mode, the code creates a new background image and tries to paste the original image onto it before converting it to RGB mode. However, the `paste` method is used incorrectly causing the bug. The `paste` method should be passed a tuple `(0, 0)` instead of the `image` variable to correctly paste the original image onto the background image.

### Fix Strategy:
1. Correct the `paste` method to use `(0, 0)` instead of `image` as the second argument.
2. Ensure that the conversion logic is properly handled for both PNG format and RGBA mode images.

### Corrected Function:
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0))  # Correcting the paste method argument
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

By making this change, the `convert_image` function is corrected to properly handle images with PNG format and RGBA mode without causing an error, ensuring that the failing tests now pass.