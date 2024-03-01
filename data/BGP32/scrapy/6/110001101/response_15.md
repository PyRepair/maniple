### Bug Explanation
The bug in the `convert_image` function is that when the image format is 'PNG' and the mode is 'RGBA', the code attempts to create a new image with a white background and paste the original image onto it. However, in the `paste` method, the second parameter should be a tuple representing the position at which to paste the image, not the image itself. This leads to an error and incorrect behavior.

### Fix Strategy
To fix the bug, we need to change the line `background.paste(image, image)` to `background.paste(image, (0, 0))`, ensuring that we paste the original image at the top-left corner of the white background image.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Fix: Changed the paste method parameter
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

With this correction, the `convert_image` function should now correctly handle images with 'PNG' format and 'RGBA' mode.