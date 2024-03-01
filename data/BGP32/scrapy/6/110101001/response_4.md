### Bug Explanation
The bug in the `convert_image` function arises from the condition that checks if the image format is 'PNG' and the mode is 'RGBA'. In this case, the function creates a new RGBA image called `background`, pastes the original image onto it, and then converts it to RGB. However, the mistake lies in the `background.paste(image, image)` line, where the original image is pasted onto itself instead of the newly created background image.

### Fix Strategy
To fix the bug, we need to correct the pasting operation to paste the original image onto the background image. This can be achieved by using `background.paste(image, (0, 0))` instead of `background.paste(image, image)`.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Fix: Pasting the image onto the background correctly
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

By making this change, the `convert_image` function should now correctly handle images with format 'PNG' and mode 'RGBA' without encountering the bug that was causing the failing test cases.