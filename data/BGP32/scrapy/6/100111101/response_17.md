### Bug Explanation
The bug in the `convert_image` function lies in the logic handling images with a format of `'PNG'` and mode of `'RGBA'`. When encountering such images, the function creates a new RGBA background image filled with white, pastes the original image onto this background, and then converts the resulting image to RGB. However, when pasting the original image onto the background, the incorrect parameter `image` is passed instead of the correct `image` value. This leads to an issue where the original image is not pasted onto the background as intended, resulting in an incorrect conversion to RGB.

### Bug Fix Strategy
To fix the bug, the function needs to correctly paste the original image onto the background. By passing the `image` object itself (instead of `image` tuple) as the second argument to the `paste` function, the bug can be addressed. Additionally, the background creation for PNG images should only be done when the mode is 'RGBA', not when the format is 'PNG' alone.

### The Corrected Function
Based on the identified bug, here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
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

By correctly pasting the image onto the background with `(0, 0)` coordinates and the image itself, we resolve the bug and ensure that the correct conversions are made for PNG images with RGBA mode.