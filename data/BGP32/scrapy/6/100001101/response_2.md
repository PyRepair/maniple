### Bug Explanation
The bug occurs when the input image has format 'PNG' and mode 'RGBA'. In this case, the function creates a new image named `background` with mode 'RGBA' and pastes the original image onto the new image. Then it converts the new image to mode 'RGB'. However, the `paste()` method requires a mode compatible with the background image, so the conversion to 'RGB' is redundant and causes loss of data.

### Fix Strategy
Instead of converting the `background` image to 'RGB', we can directly use the `image.convert()` method to convert the original image to 'RGB' if needed. This way, we avoid the unnecessary conversion and preserve the data.

### Corrected Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image.split()[3])
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