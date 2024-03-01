### Bug Explanation
The bug in the `convert_image` function lies in the condition where it checks if the image format is 'PNG' and mode is 'RGBA'. When the condition is met, it is trying to create a new background Image with RGBA mode and paste the image on it, and then convert the image to RGB mode. However, there is an issue when pasting the image onto the background due to the incorrect usage of the `paste` method. This results in the image not being pasted correctly onto the background.

### Bug Fix Strategy
To fix the bug, we need to correctly paste the image onto the background. The correct method to achieve this is by using the `paste` method with the correct parameters. The `paste` method takes a tuple as the second argument representing the position to paste the image. 

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Corrected the paste method with position
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

With this corrected version, the buggy function should now correctly handle the case where the image format is 'PNG' and mode is 'RGBA'.