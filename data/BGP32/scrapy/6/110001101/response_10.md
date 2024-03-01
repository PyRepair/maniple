### Bug Explanation
The bug in the `convert_image` function arises from the incorrect condition check for image format and mode. In the current implementation, if the image format is `'PNG'` and the mode is `'RGBA'`, it tries to convert the image to a new RGB image with a white background. However, the condition check for PNG should be case-insensitive, but it is currently checking for `'PNG'` specifically, leading to unforeseen issues.

### Bug Fix Strategy
To fix the bug, we need to make the format check case-insensitive by converting the format to lowercase before comparison. This will ensure that both `'PNG'` and `'png'` formats are correctly handled.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format.lower() == 'png' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, image)
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