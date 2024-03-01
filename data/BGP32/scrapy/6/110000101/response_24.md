### Bug Explanation:
The bug in the `convert_image` function arises from the line `background.paste(image, image)` when checking for the condition `image.format == 'PNG' and image.mode == 'RGBA'`. Here, the `paste` method requires a tuple `(x, y)` for the position argument, but it is mistakenly called with the image object `image` twice.

### Bug Fix Strategy:
To fix the bug, we need to provide the correct position argument for the `paste` method by passing `(0, 0)` instead of the second `image` argument. This will correctly paste the `image` onto the `background`.

### Corrected Version of the Function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Fix: Pass correct position argument for Image.paste
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