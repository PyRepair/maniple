### Bug Explanation
The bug in the `convert_image` function lies in the conditional check for PNG images with RGBA mode. When the image format is PNG and the mode is RGBA, the function creates a new RGBA image to paste the original image on it, creating a white background. However, when pasting the original image on the background, the `background.paste(image, image)` line has an issue. Instead of referencing the original image (`image`), it mistakenly references the background itself, resulting in an unintended conversion to RGB mode.

### Bug Fix Strategy
To fix the bug, we need to correct the line `background.paste(image, image)` to `background.paste(image, (0, 0, image.size[0], image.size[1]))`. This change ensures that the original image is correctly pasted onto the background, preserving the RGBA mode.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0, image.size[0], image.size[1]))
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

With this correction, the `convert_image` function should now properly handle PNG images with RGBA mode and maintain the transparency and color data during image conversion.