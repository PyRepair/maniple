### Bug Explanation
The buggy function `convert_image` inappropriately handles images with transparency. When the input image format is 'PNG' and mode is 'RGBA', the function does not correctly convert the image to remove transparency, causing the tests to fail.

### Bug Fix Strategy
To fix the bug, we need to correctly handle images with transparency, converting them to remove the alpha channel. We should check for 'PNG' format and 'RGBA' mode, remove transparency as a white background, and then convert the image to RGB mode.

### Corrected Version of the Function

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        # Create a white background image
        background = Image.new('RGB', image.size, (255, 255, 255))
        # Combine the original image (with transparency) and the white background
        background.paste(image, (0, 0), image)
        # Convert the combined image to RGB mode
        image = background.convert('RGB')
    else:
        # For other modes, simply convert to RGB
        image = image.convert('RGB')

    if size:
        # Resize the image if size is provided
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making the changes outlined above, the corrected version of the function should now handle images with transparency correctly and pass the failing test cases.