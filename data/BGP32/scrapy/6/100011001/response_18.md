### Bug in the Buggy Function
The bug in the `convert_image` function lies in the handling of images with transparency (alpha channel). When the input image has the format 'PNG' and mode 'RGBA', the function is supposed to remove the alpha channel and convert it to RGB. However, in the buggy implementation, the alpha channel removal is not done correctly, leading to incorrect output and failing test cases.

### Bug Fix Strategy
To fix the bug, we need to ensure that when the input image is in RGBA mode, we correctly convert it to RGB mode by creating a new image without the alpha channel. This can be achieved using the `convert` method provided by the PIL library.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        # Remove alpha channel and convert to RGB
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        # Convert to RGB if not already in RGB mode
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By correcting the conversion logic for images in RGBA mode, the function should now handle transparency correctly and produce the expected output for the provided test cases.