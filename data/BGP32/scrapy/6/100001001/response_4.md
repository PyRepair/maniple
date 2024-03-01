### Bug Explanation
The buggy function `convert_image` has an issue when dealing with images of format 'PNG' and mode 'RGBA'. It attempts to convert such images to RGB mode by creating a new RGBA background and pasting the original image onto it. However, the `paste` method should be called with a tuple specifying the position, not the image itself. This results in the background not being set correctly, leading to incorrect conversions for 'RGBA' images.

### Bug Fix
To fix the bug, modify the `paste` line to pass the correct arguments while creating the new background image for 'PNG' images with mode 'RGBA'. Additionally, ensure that the image conversion logic is consistent and handles all scenarios properly.

### Corrected Version
```python
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