### Bug Explanation:
The bug in the `convert_image` function arises from the incorrect handling of images with a format of 'PNG' and a mode of 'RGBA'. When encountering such images, the code attempts to convert the image to RGB format by creating a new background, pasting the original image onto it, and converting it to RGB. However, the code incorrectly uses `background.paste(image, image)` instead of `background.paste(image, (0, 0, image.width, image.height))`, which results in the pasting operation failing and leading to unexpected behavior.

### Bug Fix Strategy:
To fix the bug, we need to modify the portion of the code that deals with images of 'PNG' format and 'RGBA' mode. By correcting the pasting operation using the correct syntax, the function will perform the intended conversion to RGB format for such images.

### Corrected Version of the Function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0, image.width, image.height))  # Corrected pasting operation
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

By making this correction, the `convert_image` function should now handle images with a format of 'PNG' and a mode of 'RGBA' correctly, ensuring that the pasting operation is done accurately, leading to the expected behavior in the failing test cases.