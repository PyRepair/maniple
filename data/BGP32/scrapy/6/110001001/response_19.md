### Bug Explanation
The bug in the `convert_image` function arises from the condition that checks if the image format is 'PNG' and the mode is 'RGBA'. If this condition is true, the function creates a new image called `background`, pastes the original image onto it, and converts it to 'RGB'. However, the bug is that the `paste` method is incorrectly called with the same image as both arguments, causing the image to not be pasted correctly onto the background image.

### Bug Fix
To fix the bug, we need to correct the `paste` method call by providing the correct arguments. Here is the corrected version of the `convert_image` function:
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

By providing the correct arguments to the `paste` method, the bug is fixed and the function should work as intended now.