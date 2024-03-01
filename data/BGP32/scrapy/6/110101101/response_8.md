### Bug Explanation
The bug in the `convert_image` function is caused by incorrect handling of PNG images with RGBA mode. When the input image is a PNG with RGBA mode, the function is attempting to paste the image onto a new background with RGBA mode, resulting in loss of transparency. This leads to incorrect conversion to RGB mode.

### Fix Strategy
To fix the bug, the function should check for PNG images with RGBA mode, create a new image background with RGB mode, paste the input image onto the new background, and then convert the image to RGB mode before proceeding with thumbnail generation.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
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

After applying this correction, the function should now correctly handle the conversion of PNG images with RGBA mode and generate thumbnails while maintaining transparency.