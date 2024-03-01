### Analysis:
The buggy function `convert_image` is responsible for converting images to JPEG format and resizing them if a size parameter is provided. However, there are issues in the function that need to be addressed:
1. The condition to handle PNG images with RGBA mode is incorrect. It should be checking for PNG format instead of JPEG since it is trying to convert PNG with RGBA to RGB.
2. In the case where a size parameter is provided, the function resizes the image but does not update the size attribute accordingly.
3. The function mistakenly saves the image in JPEG format regardless of the original format of the input image.

### Strategy:
1. Update the conditional check for PNG with RGBA mode to properly identify and convert such images.
2. Update the size of the resized image to reflect the new dimensions correctly.
3. Save the image in the input format instead of always saving it as JPEG.

### Updated Code:
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

# The declaration of the class containing the buggy function
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background.convert('RGB')
        elif image.format != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
            image.size = size

        buf = BytesIO()
        image.save(buf, image.format)
        return image, buf
``` 

The above corrections address the identified issues and ensure that the function behaves as expected based on the specified input/output values.