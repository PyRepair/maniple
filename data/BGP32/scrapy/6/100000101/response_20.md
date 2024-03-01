The buggy function has a few issues that need to be addressed:

1. The conditional check for PNG images with RGBA mode is incorrect. It should convert PNG images with RGBA mode to RGB, not to JPEG.
2. When pasting the image onto a background with paste, the correct method is to use 'paste' with 'RGBA' mode.
3. When converting images, the correct mode to convert to is 'RGBA' for PNG images with RGBA mode, not 'RGB'.

To fix these issues, we need to make the following adjustments:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA': 
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background.convert('RGBA')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making these adjustments, the function should now properly handle PNG images with RGBA mode and convert them to RGB, as well as handle other image modes correctly.