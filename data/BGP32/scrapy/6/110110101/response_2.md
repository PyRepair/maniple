### Analysis
1. **Buggy Function**: The `convert_image` function is supposed to convert images to RGB and create thumbnails if specified.
   
2. **Issues**:
   - The code contains a bug in handling PNG images with RGBA mode. It tries to create a new image with a white background to handle transparency but pastes the image on itself, which causes the background to be transparent instead of creating a white background.
   - The conversion process for RGBA images to RGB mode is incorrect.
   - The image format being saved is hardcoded as JPEG instead of using the input image format.

3. **Bug Cause**:
   When handling PNG images with RGBA mode, the incorrect background creation and pasting cause the transparency issue. This results in the comparison failure in the test case due to different color values.

4. **Strategy for Fixing the Bug**:
   - Create a new background image with a white color.
   - Paste the original image on the background image correctly.
   - Correctly convert RGBA images to RGB by removing the background-related logic.
   - Save the image in the correct format based on the input image format.

### Corrected Version
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implements the image thumbnail generation logic
    """

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
        image.save(buf, image.format)
        return image, buf
```

By fixing the background creation and pasting, correcting the RGBA to RGB conversion, and saving the image in the correct format, the `convert_image` function should now handle the specified image types and sizes correctly.