The bug in the `convert_image` function stems from the way the background image is pasted in the case where the input image has a format of 'PNG' and mode 'RGBA'. By pasting the image with the same coordinates (image, image), it creates unnecessary blending issues. The correct approach is to paste the image onto the background image.

To fix the bug, we need to update the way the `background.paste` method is called in this specific case. We also need to ensure that when converting an image with a format of 'PNG' and mode 'RGBA' to 'RGB', we handle transparency properly.

Here is the corrected version of the `convert_image` function:

```python
from PIL import Image
from cStringIO import StringIO as BytesIO

class ImagesPipeline(FilesPipeline):
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

With this fix, the specific issue with pasting the background in the case of 'PNG' and 'RGBA' images should be resolved, and the function should be able to handle the transparency correctly. The corrected version should now pass the failing test cases provided.