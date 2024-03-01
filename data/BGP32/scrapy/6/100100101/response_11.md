### Bug Explanation
The bug in the `convert_image` function lies in the condition `if image.format == 'PNG' and image.mode == 'RGBA'`. This condition assumes that an image with format 'PNG' will have a mode of 'RGBA', which may not always be true. As a result, the code creates a new background image with RGBA mode and tries to paste the original image onto it, which results in an inconsistency when saving the image as JPEG.

### Bug Fix Strategy
To fix the bug, we need to revise the condition that checks for PNG format and RGBA mode. The code should handle transparent images correctly and save them as JPEG images without losing the original transparency. 

One way to fix this is to consider checking if an image has an alpha channel (transparency) instead of strictly checking for RGBA mode when the format is PNG. If the image has an alpha channel, preserve the transparency when converting and saving the image as JPEG.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and 'A' in image.getbands():
        image = image.convert('RGBA')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

This corrected version of the function checks if the image has an alpha channel ('A' in image.getbands()) for PNG images. If the image has an alpha channel, it is converted to RGBA to preserve transparency. The function should now handle transparent PNG images properly without losing the transparency when saving as JPEG.