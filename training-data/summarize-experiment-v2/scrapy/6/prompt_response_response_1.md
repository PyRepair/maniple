Here is the corrected version of the buggy function:

```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
    
        if size:
            image = image.resize(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

In the corrected version of the function:
1. The bug causing the discrepancies in the failing test cases is fixed by creating a new RGB background image instead of RGBA and then pasting the original image onto it, as well as fixing the resizing logic.
2. The changes are based on input and output variable information from the failing test cases.

After making these changes, the function should now correctly execute the image transformations and pass the failing test cases.