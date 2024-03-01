### Issues/ Analysis:
There are a few issues in the `convert_image` function:
1. The conditional check for PNG format and RGBA mode in the first if block is checking for uppercase 'PNG'. However, the format returned by the Image object is lowercase. Hence, the condition will never be satisfied, leading to incorrect handling of images in RGBA mode.
2. In the second if block, when checking if the image mode is not RGB, the conversion of the image to RGB is incorrect. It should convert directly to RGB instead of copying the image and then converting.
3. The conversion to JPEG format at the end is hardcoded, which might not be suitable for all cases.

### Fix Strategy:
1. Correct the conditional check for PNG format to lowercase.
2. Modify the conversion logic for images that are not in RGB mode to directly convert to RGB.
3. Allow for specifying the output format of the image.

### Corrected Version of the Function:
```python
from PIL import Image
from cStringIO import StringIO as BytesIO
from io import BytesIO as BytesIO
from PIL import Image

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    
    """

    def convert_image(self, image, size=None, output_format='JPEG'):
        if image.format.lower() == 'png' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        if size:
            image.thumbnail(size, Image.ANTIALIAS)
        
        buf = BytesIO()
        image.save(buf, output_format)
        return image, buf
```

### Changes Made:
1. Fixed the conditional check for PNG format by using `image.format.lower()`.
2. Modified the image conversion logic to directly convert to RGB if the mode is not RGB.
3. Added a parameter `output_format` to specify the format in which the image should be saved.