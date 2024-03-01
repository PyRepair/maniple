### Explanation:
The bug in the `convert_image` function is related to the handling of images with transparency (alpha channel) in the PNG format. When the input image format is PNG and the mode is RGBA, the function incorrectly tries to create a new image with a white background and paste the original image onto it. This operation does not correctly handle the transparency information, leading to incorrect results.

### Bug:
The bug is caused by the incorrect handling of images with transparency (alpha channel) in the PNG format. The function incorrectly converts the RGBA image to RGB without preserving the transparency information.

### Strategy for fixing the bug:
1. Check if the input image is in PNG format and has an RGBA mode.
2. If the above conditions are met, convert the image to RGB mode while preserving the transparency information.
3. Make sure to handle images with transparency correctly when creating thumbnails.

### Corrected version of the function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB', background=(255, 255, 255))
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By following the above steps and correcting the `convert_image` function, images with transparency will be handled correctly when converting to RGB mode for PNG images with RGBA mode. This correction should make the function pass the failing tests.