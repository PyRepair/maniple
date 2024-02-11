# BUGGY FUNCTION FIX

Here's the corrected version of the buggy function:

```python
from PIL import Image
from io import BytesIO

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, format="JPEG")
        return image, buf
```

Changes made:
1. Replaced the import statement for BytesIO to import from io.
2. Updated the conversion of RGBA images to RGB by specifying the correct region to paste the image.
3. Changed the import of BytesIO to ensure compatibility.
4. Specified the format parameter as "JPEG" in the image.save method.

The corrected function should now handle the image conversions and resizing correctly, resolving the issues in the failing test cases.