### Bug Explanation
The bug in the `convert_image` function lies in the condition that checks for `'PNG'` format and `'RGBA'` mode, the subsequent conversion to RGB loses alpha values without preserving transparency.

### Bug Fix Strategy
To resolve the bug, we need to ensure that transparency is preserved when converting from RGBA to RGB. We can achieve this by creating a white background with the same size as the image and then pasting the image onto it, preserving any transparency values.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))  # RGBA white background
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

With this correction, the function will correctly handle images with transparency, ensuring that alpha values are preserved during conversion from RGBA to RGB.