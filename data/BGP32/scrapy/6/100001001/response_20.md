### Explanation:
The buggy function is not correctly handling images with 'PNG' format and 'RGBA' mode. The bug occurs when the function tries to convert the image to 'RGB' after pasting it on a white background. This background image should be in 'RGB' mode instead of 'RGBA'.

### Bug Fix:
To fix the bug, the function needs to create a white background image in 'RGB' mode and then paste the original image onto it. Here is the corrected version of the function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
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

This fix ensures that the white background is created in 'RGB' mode before pasting the image.