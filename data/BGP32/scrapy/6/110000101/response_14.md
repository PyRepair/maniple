### Explanation:
The bug in the provided function `convert_image` lies in the conditional statement that aims to convert images with 'PNG' format and 'RGBA' mode to 'RGB' format. The condition `image.format == 'PNG' and image.mode == 'RGBA'` is incorrectly checking the image format and mode. The `format` attribute of the Image object does not represent the file format but the actual image mode/format (e.g., 'RGB', 'RGBA', 'P', etc.), which is why the condition is not correctly identifying images with 'PNG' format and 'RGBA' mode.

### Bug Fix Strategy:
1. We should modify the condition to check the actual image mode in the correct way.
2. Instead of checking `image.format` for 'JPEG', we should directly convert the image using a more robust approach.

### Corrected Version:
```python
from PIL import Image
from cStringIO import StringIO as BytesIO
from scrapy.pipelines.files import FilesPipeline

class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    
        
    """

    def convert_image(self, image, size=None):
        if image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        else:
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

By correcting the condition and directly converting the image in a more robust way, the function should now work correctly with the expected inputs and outputs mentioned in the provided test cases.