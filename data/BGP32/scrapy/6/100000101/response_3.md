The bug in the provided function is caused by incorrect handling of the image conversion and resizing logic. The buggy function has issues in converting images with RGBA format to RGB and resizing images. 

To fix the bug, we need to ensure that when the input image has PNG format and RGBA mode, it is converted to RGB format before resizing. Additionally, we need to fix the logic for resizing the images using the provided size parameter.

Here is the corrected version of the function:

```python
from PIL import Image
from io import BytesIO

def convert_image(image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0))
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.resize(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

This corrected version of the function should now properly handle the conversion of images from PNG with RGBA mode to RGB format when needed and resize the images correctly according to the provided size parameter.

It should now satisfy all the expected input/output values for the given test cases.