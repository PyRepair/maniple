### Bug Explanation
The bug in the `convert_image` function arises from the condition for handling PNG images with an RGBA mode. The bug incorrectly assumes that the background should be filled with white color when pasting the RGBA image, leading to an incorrect output when converting to RGB.

### Bug Fix Strategy
To fix the bug, we need to ensure that when handling PNG images with RGBA mode, we correctly convert the image to RGB without altering the background color.

### Corrected Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

By updating the `convert_image` function as shown above, we ensure that PNG images with RGBA mode are correctly converted to RGB without altering the background color, thus fixing the bug.