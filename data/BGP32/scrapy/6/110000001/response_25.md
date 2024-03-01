## Analysis:
1. The buggy function `convert_image` in the `ImagesPipeline` class is supposed to convert an image to a specified format and size. 
2. The potential error locations in the function could be the image format check and the conversion logic.
3. The bug occurs when the image format is 'PNG' and mode is 'RGBA', as it should be converted to 'RGB' before resizing. However, the conversion is not being done correctly leading to the bug.
4. To fix the bug, we need to handle the 'PNG' with 'RGBA' case separately to convert it to 'RGB' before resizing the image.

## Fixed Version:

```python
class ImagesPipeline(FilesPipeline):
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, (0, 0), mask=image.split()[3])
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

In the corrected version:
- We handle the case when the image format is 'PNG' and mode is 'RGBA' separately by creating a new 'RGB' image with a white background, pasting the original image with the alpha channel, and converting the image to 'RGB'.
- The conversion logic has been adjusted to correctly handle the 'PNG' with 'RGBA' case before resizing.
- The function should now work correctly for converting and resizing images.