## Bug Explanation
The bug in the `convert_image` function is that the conditional statement to convert the image to RGB format when the input format is PNG and mode is RGBA is not working as expected. The `background.paste(image, image)` line is not correctly pasting the original image onto the new background image. This results in an incorrect conversion to RGB format.

## Bug Fix
To fix the bug, we need to correct the way the original image is pasted onto the background image. Instead of `background.paste(image, image)`, we should use `background.paste(image, (0, 0), image)`. This will correctly paste the original image onto the new background image.

## Corrected Version
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