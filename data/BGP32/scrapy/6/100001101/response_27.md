### Bug Explanation
The bug in the `convert_image` function occurs due to incorrect handling of the image format and mode. When the input image is in PNG format and RGBA mode, the function incorrectly converts it to RGB format without preserving transparency. This leads to a loss of information and incorrect conversion of the image.

### Bug Fix Strategy
To fix this bug, we need to ensure that when the input image is in PNG format and RGBA mode, it is converted correctly to RGB format while preserving transparency. This can be achieved by creating a new RGBA image with a white background and then pasting the original PNG image onto it before converting it to RGB.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
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

With this correction, the function will correctly handle PNG images with RGBA mode by preserving transparency during the conversion to RGB format.