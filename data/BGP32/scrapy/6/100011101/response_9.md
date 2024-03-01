### Bug Explanation
The bug in the `convert_image` function arises from incorrectly handling images with transparency (alpha channel). When the input image's mode is RGBA and format is PNG, the function tries to paste the image onto a new RGBA background filled with white (255, 255, 255) color before converting it to RGB. The `paste` method attaches the alpha channel as well, resulting in an incorrect conversion.

### Bug Fix Strategy
To fix the bug, we need to remove the alpha channel from the RGBA image before pasting it onto a white background. This can be achieved by converting the input image to RGB mode before pasting it onto the background.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image.convert('RGB'), (0, 0), image)
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

After applying the correction, the function should now correctly handle images with transparency and convert them to RGB without the alpha channel information. This should resolve the failing tests and achieve the expected input/output values.