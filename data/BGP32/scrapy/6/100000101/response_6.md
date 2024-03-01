The bug in the function `convert_image` comes from the incorrect handling of the PNG images with RGBA mode. The function is trying to create a new RGB image from the original RGBA image by pasting it on a white background, but the `paste` method does not work as intended in this context.

To fix this bug, we can create a new RGB image from the RGBA image using the `convert` method directly. Additionally, we need to handle the case when the input image is already in RGB mode.

Here is the corrected version of the function:

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

This corrected version handles the conversion from RGBA to RGB correctly by directly converting the image. Additionally, it properly converts images to RGB mode when necessary.