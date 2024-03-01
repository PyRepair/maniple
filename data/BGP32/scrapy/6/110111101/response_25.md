### Bug Explanation:
The bug in the `convert_image` function arises from an issue with handling images that are in PNG format and have an RGBA mode. The function attempts to convert such images to RGB mode without accounting for the transparency of the original image, leading to incorrect results in the converted image.

When the input image has the format 'PNG' and the mode 'RGBA', the function creates a new background image in RGB mode, pastes the original image onto the background, and then converts the result to RGB mode. However, this process does not preserve the transparency information in the original RGBA image, resulting in incorrect color compositions in the output.

### Solution Strategy:
To fix the bug, the function needs to handle PNG images with RGBA mode differently to preserve their transparency information during the conversion to RGB mode. One way to achieve this is by using the `convert('RGB', ...)` method with a `palette` argument that specifies how to handle the transparency data.

Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB', palette=Image.ADAPTIVE, colors=255)
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

This corrected version of the function ensures that PNG images with RGBA mode are properly converted to RGB mode while preserving their transparency information. This should fix the issues observed in the failing tests.