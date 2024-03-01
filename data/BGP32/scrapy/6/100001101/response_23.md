### Bug Explanation
The bug in the provided function lies in the condition that checks if the image format is 'PNG' and the mode is 'RGBA'. The buggy function incorrectly handles the condition by converting the image to RGB without preserving transparency.

### Bug Fix Strategy
To fix the bug, we need to modify the code within the first conditional block to maintain the transparency of the image when converting it to RGB. This can be achieved by creating a new RGBA image with a white background and overlaying the original RGBA image on top of it. Then, converting the resulting image to RGB.

### Corrected Function
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

By creating a new RGBA image with a white background and correctly overlaying the original RGBA image on top of it, the corrected function now ensures that the transparency of the image is maintained when converting it to RGB.