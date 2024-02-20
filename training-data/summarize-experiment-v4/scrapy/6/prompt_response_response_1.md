## Bug Cause

The bug is caused by the incorrect handling of transparent RGBA images in the `convert_image` function.
The function does not correctly handle the background when converting from PNG with RGBA mode to RGB mode.

## Approach to Fix the Bug

To fix the bug, we need to ensure that transparent RGBA images are properly converted to RGB mode without losing the transparency information.
We also need to ensure that the function correctly handles resizing and saving the image when a size parameter is provided.

## The Corrected Code

Here is the corrected code for the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)
    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

In the corrected code:
1. We removed the condition for image format and focused solely on the image mode.
2. When handling RGBA images, we directly convert them to RGB mode without creating a new background image.
3. We retained the resizing and saving functionality when a size parameter is provided.

With these changes, the function should now correctly handle transparent RGBA images and perform image resizing and saving as expected.