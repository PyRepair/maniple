### Bug Explanation
The bug in the `convert_image` function lies in the conditional check for PNG images with RGBA mode. When a PNG image with RGBA mode is encountered, the function incorrectly creates a new in-memory image (`background`) of RGBA mode filled with white color and then pastes the original image over it. Once pasted, the original image is converted to RGB mode. This process causes the transparency information from the original RGBA image to be lost, resulting in a solid white background instead of maintaining transparency.

### Bug Fix Strategy
To fix the bug, we need to preserve the transparency information when dealing with PNG images with RGBA mode. This can be done by checking if the input image format is PNG and if it has RGBA mode. In this case, we should directly convert the image to RGB while preserving the alpha channel.

### Corrected Function
Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB')  # Convert directly to RGB while preserving alpha
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making this change, we ensure that PNG images with RGBA mode retain their transparency when converted to RGB, addressing the bug in the original function.