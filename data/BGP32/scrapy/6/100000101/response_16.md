The buggy function has a few issues:
1. The condition for converting PNG images with RGBA mode to RGB mode is incorrect. It should check if the image format is 'PNG' and mode is 'RGBA', not just 'PNG'.
2. When pasting the original image onto a new background, the paste function should have two arguments: the image object and a tuple specifying the coordinates for pasting.

To fix the bug, we need to:
1. Correct the condition for converting PNG images with RGBA mode to RGB mode.
2. Properly paste the original image onto a new background by providing the correct arguments to the paste function.

Here is the corrected version of the function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))
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