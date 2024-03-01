### Bug Explanation
The bug in the `convert_image` function lies in the condition to check for PNG format and RGBA mode images. The code inside that condition is supposed to convert such images to RGB format by pasting the image onto a new RGBA background. However, the `background.paste(image, image)` line is incorrect. The correct way to paste the image onto the background is `background.paste(image, (0, 0), image)`. This bug causes the function to behave incorrectly for PNG images with RGBA mode.

### Fix Strategy
To fix the bug, we need to update the line `background.paste(image, image)` to `background.paste(image, (0, 0), image)` to correctly paste the image onto the background.

### Corrected Version of the Function
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

By making this change, the function will correctly handle PNG images with RGBA mode and ensure that the image is converted to the RGB format as expected.