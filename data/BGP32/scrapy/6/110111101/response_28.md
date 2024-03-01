### Bug Explanation
The bug in the `convert_image` function is that when the image format is 'PNG' and the mode is 'RGBA', it attempts to create a new image with a white background and paste the existing image onto it with alpha blending. However, the `paste` function is called incorrectly, resulting in the original image being pasted over itself (instead of the background image), leading to incorrect color values when converting to 'RGB'.

### Bug Fix Strategy
1. When the image format is 'PNG' and the mode is 'RGBA', create a new background image with the correct size and paste the original image onto it with the alpha channel.
2. Make sure to return the corrected image and the buffer containing the image data after saving it as 'JPEG'.

### Corrected Version

```python
def convert_image(self, image, size=None):
    if image.mode == 'RGBA' and image.format == 'PNG':
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

By correcting the paste method arguments to specify the position `(0, 0)` to paste the image correctly on the background, the bug is fixed, and the function now correctly converts images with transparency to 'RGB' format while maintaining the expected colors.