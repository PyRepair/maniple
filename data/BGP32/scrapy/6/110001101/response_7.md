### Bug Explanation
The bug in the `convert_image` function arises from the incorrect handling of images with RGBA mode and PNG format. The function checks if the image format is PNG and mode is RGBA, then converts the image to RGB by creating a new RGB image with a white background and pasting the original image onto it. However, the `background.paste(image, image)` call is incorrect as it should be `background.paste(image, (0, 0), image)`. This mistake leads to the creation of an all-white image instead of correctly pasting the original image onto the background.

### Fix Strategy
To fix the bug, we need to modify the line `background.paste(image, image)` to `background.paste(image, (0, 0), image)` in the case where the image format is PNG and mode is RGBA. This change ensures that the original image is correctly resized and pasted onto the new RGB image with a white background.

### Corrected Version
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