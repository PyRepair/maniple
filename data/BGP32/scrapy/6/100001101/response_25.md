### Bug Explanation:
The bug in the function is due to the if condition that checks if the image format is 'PNG' and the mode is 'RGBA'. However, the condition should instead check if the image format is 'RGBA' and the mode is 'RGBA'. This is causing the function to create a new background image unnecessarily and convert it to RGB format when it shouldn't.

Additionally, when converting an image to RGB format, the `paste()` method shouldn't be used, as it incorrectly pastes the original image onto a white background, which is not the intended behavior.

### Bug Fix Strategy:
1. Change the if condition to check if the image format is 'RGBA' and the mode is 'RGBA'.
2. Instead of using the `paste()` method, directly convert the RGBA image to RGB format.

### The Corrected Function:
```python
def convert_image(self, image, size=None):
    if image.format == 'RGBA' and image.mode == 'RGBA':
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