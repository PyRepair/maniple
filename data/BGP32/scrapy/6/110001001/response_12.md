### Explanation:
The buggy function `convert_image` has a logic error where if the image format is `'PNG'` and the mode is `'RGBA'`, it should convert the image to RGB format by pasting it on a new RGB background. However, the current implementation has a mistake in how the image is pasted onto the background. 

In the buggy function:
1. When the image format is `'PNG'` and mode is `'RGBA'`, a new RGBA background is created.
2. The image is pasted onto this background using `background.paste(image, image)`. The correct call should be `background.paste(image, (0, 0), image)`. The mistake here is that the image itself is passed as the second argument instead of the position `(0, 0)`.
3. The image is then converted to RGB if the mode is not `'RGB'`.
4. If a `size` parameter is provided, the image is resized.
5. Finally, the image is saved to a BytesIO buffer in JPEG format.

### Fix: 
To fix the bug, we need to correct the way the image is pasted onto the new background when the image format is `'PNG'` and mode is `'RGBA'`.

Here's the corrected version of the `convert_image` function:

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

With this fix, the image should now be pasted correctly onto the new background when needed.