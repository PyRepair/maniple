The bug in the `convert_image` function arises from the condition checking for PNG format and RGBA mode images. The bug occurs because the `image.format` property is case-sensitive, so checking for `'PNG'` while the actual format might be `'png'` leads to incorrect results.

To fix this bug, we need to correct the condition check for PNG format images to be case-insensitive. We can achieve this by converting both the `image.format` and the comparison string to lowercase before comparison. Additionally, we need to ensure that the mode is converted to RGB only if it's RGBA to avoid unnecessary conversions.

Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format.lower() == 'png' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, image)
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

This corrected version accounts for case sensitivity when checking the image format and properly handles the conversion of image modes to RGB only when necessary.