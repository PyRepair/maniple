### Bug Explanation
The bug in the `convert_image` function occurs due to incorrect handling of the image format and mode conditions. Specifically, the condition to convert RGBA format images to RGB format is incorrect. The buggy code checks for PNG format images with RGBA mode for conversion to RGB, which is incorrect. This results in incorrect image conversion and hence failing the test cases that expect specific modes.

### Bug Fix Strategy
1. Update the condition for RGBA conversion to RGB to include all formats (not just PNG).
2. Handle the conversion based on the image mode correctly for all formats.
3. Ensure that the thumbnail generation maintains the correct image ratio.

### Corrected Function
```python
def convert_image(self, image, size=None):
    if (image.mode == 'RGBA' and image.mode == 'P') or (image.mode != 'RGB'):
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making the above changes, the function should now correctly handle different image formats and modes, ensuring that the test cases pass with the expected values.