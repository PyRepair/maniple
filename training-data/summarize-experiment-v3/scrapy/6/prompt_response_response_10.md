## Bug's Cause

The bug is caused by incorrect handling of image format and mode within the `convert_image` function. The function does not create a new background image as intended and does not properly handle the conversion of images to RGB format. Additionally, when a size parameter is provided, the function does not create a new image with the correct size.

## Approach to Fix the Bug

To fix the bug, the `convert_image` function needs to be modified to correctly handle the creation of a new background image, ensure proper conversion of images to RGB format, and correctly handle the resizing of images when a size parameter is provided.

## The corrected code for the buggy function

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

With these changes, the function should correctly handle the creation of a new background image, the conversion of images to RGB format, and the resizing of images when a size parameter is provided.