### Bug Explanation
The buggy function `convert_image` has an issue where it does not correctly handle images with RGBA mode and PNG format. When the input image has format 'PNG' and mode 'RGBA', it attempts to convert it to RGB by creating a new image with a white background and pasting the original image on top of it. However, the paste operation is done incorrectly, resulting in the background image being dominant and the final image being all white instead of maintaining the original image content.

### Bug Fix Strategy
To fix the bug, the incorrect paste operation when dealing with 'PNG' format and 'RGBA' mode images needs to be corrected. Instead of using `background.paste(image, image)`, we should use `background.paste(image, (0, 0), image)`. This ensures that the original image is correctly pasted on top of the white background.

### Corrected Version of the Function
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

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
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

By making this correction to the paste operation, the function should now properly handle PNG images with RGBA mode and pass the failing test cases.