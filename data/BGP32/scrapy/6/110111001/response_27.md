### Bug Explanation
The bug occurs in the `convert_image` function when handling images with format 'PNG' and mode 'RGBA'. In this case, a new image with mode 'RGBA' is created as the background, and instead of using `background.paste(image, image)` to paste the original image onto the background, `background.paste(image, image)` is pasting the background onto itself. This results in the output image being incorrect and causing the test to fail.

### Bug Fix
To fix the bug, we need to correct the paste operation inside the condition where the image format is 'PNG' and mode is 'RGBA'. The correct operation should be `background.paste(image, (0, 0), image)`, which correctly pastes the original image onto the background.

### Corrected Function
```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
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

By correcting the paste operation in the 'PNG' and 'RGBA' condition, the function should now correctly process images and pass the failing test cases.