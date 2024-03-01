### Bug Analysis:
The bug in the `convert_image` function lies in the conditional statement that checks if the input image format is 'PNG' and the mode is 'RGBA'. In this case, it attempts to create a new background image with RGBA mode and paste the input image onto it. However, when pasting the image, it should reference the input image instead of passing it as an argument to `background.paste()`. This results in not properly pasting the image onto the background and converting it to RGB mode incorrectly. 

### Bug Fix Strategy:
1. Update the line `background.paste(image, image)` to `background.paste(image, (0, 0, image.size[0], image.size[1]))` to properly paste the input image onto the background.
2. Update the line `image = background.convert('RGB')` to `image = background` to retain the image with RGBA mode and the correct pasted content.

### Corrected Version:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0, image.size[0], image.size[0]))
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

By making these changes, the `convert_image` function should now properly handle images in RGBA mode when the format is 'PNG' and pass the failing tests.