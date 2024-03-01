### Bug Explanation:
The bug in the `convert_image` function lies in how the image is processed when its format is `'PNG'` and its mode is `'RGBA'`. The function attempts to convert such images to `'RGB'` by creating a new `background` image with a white background and pasting the original image on top of it. However, the mistake is in how the original image is pasted onto the background. It should use the `paste` method on the `background` image, but instead, it passes `image` as the second argument to `paste`, which effectively pastes the image onto itself.

This results in the `image` variable being incorrectly processed and saved as `'RGB'` format without the intended operation of pasting on the background.

### Fix Strategy:
To fix this bug, we need to correctly paste the original image onto the background image when the format is `'PNG'` and mode is `'RGBA'`. This can be achieved by modifying the line `background.paste(image, image)` to `background.paste(image, (0, 0, image.size[0], image.size[1]))` to correctly paste the image onto the background.

### Corrected Version of the Function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0, image.size[0], image.size[1]))
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

After applying this fix, the `convert_image` function should correctly handle images with format `'PNG'` and mode `'RGBA'`, ensuring that the pasting operation is done correctly before converting it to `'RGB'`.