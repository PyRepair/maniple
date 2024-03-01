### Bug Explanation
The bug in the `convert_image` function is due to an issue when handling images with format `'PNG'` and mode `'RGBA'`. In the conditional block where the format is `'PNG'` and mode is `'RGBA' the function is creating a new image `background` of mode `'RGBA'`, pasting the original image onto it, and then converting the whole image to mode `'RGB'`. This procedure loses the transparency information from the original image, resulting in incorrect output.

### Bug Fix Strategy
To fix the bug, we need to preserve the transparency information of images with format `'PNG'` and mode `'RGBA'`. Instead of converting the entire image to mode `'RGB'`, we need to handle transparency separately before creating a thumbnail.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
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

With this correction, the function properly handles images with transparency information and should pass the failing test cases provided.