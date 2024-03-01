### Bug Explanation
The bug in the `convert_image` function is due to an incorrect logic in handling images with transparency. When the input image format is 'PNG' and the mode is 'RGBA', the function attempts to flatten the transparency by pasting the image on a new background with opaque white color. However, the `paste` method is not used correctly, and the resulting image does not handle transparency as intended. This leads to incorrect conversions for images with transparency, causing the tests to fail.

### Bug Fix Strategy
To fix the bug, the `paste` method should be used correctly to ensure that transparency is handled properly. Additionally, the image mode should be set to 'RGB' after addressing transparency for 'PNG' images with 'RGBA' mode.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

By using the corrected version of the function above, the tests should pass successfully with the expected input/output values.