The bug in the provided function is in the if condition where it attempts to convert an image with format 'PNG' and mode 'RGBA' to an RGB image. The bug occurs when pasting the 'RGBA' image onto a new 'RGBA' background, which results in an image of mode 'RGBA' instead of 'RGB'. This causes the subsequent conversion to 'RGB' mode to be ineffective.

To fix this bug, the code snippet inside the if condition needs to be modified to correctly convert the image to 'RGB', regardless of the original image mode.

Below is the corrected version of the function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG':
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        else:
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

This correction ensures that an image with format 'PNG' is always converted to 'RGB' mode before resizing or saving, regardless of its initial mode. This modification should address the bug and satisfy all expected input/output values provided in the test cases.