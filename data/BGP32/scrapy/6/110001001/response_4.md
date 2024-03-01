### Bug Explanation
The bug in the `convert_image` function arises from the condition that checks if the image format is 'PNG' and the mode is 'RGBA'. In this case, it tries to convert the image to 'RGB' by creating a new image and pasting the original image on top of it. However, the `paste` method call is incorrect, leading to a wrong conversion.

### Bug Location
The bug is located in the following lines:
```python
background.paste(image, image)
```
The `paste` method should take a tuple representing the position where the image should be pasted, not the image itself as the second argument.

### Bug Fix Strategy
To fix the bug, we need to correct the `paste` method call by providing the correct position tuple as the second argument.

### Corrected Version
Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Corrected paste method call
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

This corrected version ensures that the `paste` method call correctly pastes the image onto the background for conversion.