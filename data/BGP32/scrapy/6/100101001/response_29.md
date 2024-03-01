### Bug Explanation
The bug in the `convert_image` function occurs because the condition to handle PNG images with RGBA mode is incorrect. When the image format is PNG and the mode is RGBA, the function is supposed to create a new RGBA background image, paste the original image onto it, and then convert it to RGB. However, the current implementation pastes the original image onto a new RGBA background, which results in an image with an incorrect mode.

### Bug Fix
To fix the bug in the `convert_image` function, we need to modify the condition for handling PNG images with RGBA mode. Instead of pasting the original image onto a new background image, we should paste it onto a RGBA background, then convert the result to RGB.

Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
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

This corrected version properly handles PNG images with RGBA mode by creating a new RGBA background image with an alpha channel and correctly pasting the original image onto it.