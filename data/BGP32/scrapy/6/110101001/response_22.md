### Bug Explanation
The bug is caused by incorrect handling of images with format 'PNG' and mode 'RGBA' in the `convert_image` function. When the input image has format 'PNG' and mode 'RGBA', the function is supposed to convert it to RGB mode and remove the alpha channel. However, the current implementation doesn't correctly handle this conversion, leading to incorrect output images.

### Bug Fix Strategy
To fix the bug, we need to ensure that when the input image has format 'PNG' and mode 'RGBA', it is properly converted to RGB mode without the alpha channel. This can be achieved by creating a new RGB image with a white background and pasting the original image onto it before converting it to RGB mode.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background
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

This corrected version ensures that images with format 'PNG' and mode 'RGBA' are properly converted to RGB mode.