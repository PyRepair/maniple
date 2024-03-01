### Bug Explanation
The bug in the `convert_image` function is related to the condition checking for PNG format and RGBA mode images. In the if statement `if image.format == 'PNG' and image.mode == 'RGBA':`, the check for the image mode 'RGBA' is incorrect. The condition should actually be `if image.format == 'PNG' and image.mode == 'RGBA' not in image.info.get("transparency", {}):`.

The issue is caused by the incorrect condition, resulting in incorrect handling of RGBA images causing the test cases to fail.

### Fix Strategy
1. Modify the condition to properly check for RGBA images with transparency information.
2. Update the logic in the function to handle RGBA images with transparency correctly.
3. Ensure that the function returns the expected RGB images after conversion.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and 'transparency' in image.info:
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