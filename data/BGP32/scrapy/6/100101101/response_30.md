### Bug Explanation
The bug in the `convert_image` function lies in the conditional statement that handles the case when the input image has format 'PNG' and mode 'RGBA'. In that case, the function creates a new RGBA background image and pastes the original image on it, expecting the transparent pixels to become white. However, this operation does not work as intended, resulting in a background filled with black color.

### Bug Fix Strategy
To fix the bug, we should update the way the background is created for the RGBA images. Instead of a white background, we should create a transparent background.

### Corrected Version of the Function
Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (0, 0, 0, 0))
        background.paste(image, image)
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

With this correction, the function now correctly creates a transparent RGBA background when needed, fixing the issue with black backgrounds for RGBA images.