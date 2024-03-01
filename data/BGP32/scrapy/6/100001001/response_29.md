### Bug Explanation
The bug in the `convert_image` function is that when the input image is in 'PNG' format and 'RGBA' mode, the function incorrectly attempts to convert the image to 'RGB' by creating a new background image with a white color and pasting the original image onto it. However, the `paste` function expects a box tuple as the second argument specifying the region to paste the image, but it receives the entire image object instead. This causes the function to produce incorrect results, such as converting 'RGBA' to 'RGB' incorrectly.

### Bug Fix
To fix the bug, we need to correct the usage of the `paste` method in the case where the image format is 'PNG' and mode is 'RGBA'. We should use a tuple specifying the paste region instead of passing the whole image object. Additionally, to avoid potential issues, we can simplify the code and remove unnecessary parts.

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
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

In the corrected version, we fixed the `paste` method in the 'PNG' and 'RGBA' case by providing a tuple `(0, 0)` as the box to correctly paste the image. This should resolve the bug and produce the intended conversion results.