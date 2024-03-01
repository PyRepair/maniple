### Bug Explanation:
The buggy function `convert_image` has a problem with the image conversion logic. It checks if the image format is 'PNG' and the mode is 'RGBA' to create a new image with a white background and then convert it to 'RGB'. However, the bug lies in the line `background.paste(image, image)` where it pastes the original image on itself instead of the created background image.

### Bug Fix Strategy:
1. Create a new background image.
2. Paste the original image on the new background image.
3. Convert the new background image to 'RGB' mode if needed.
4. Perform thumbnail resizing if a size is provided.
5. Save the image in the 'JPEG' format.

### Corrected Version of the Function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))
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

After making these changes, the corrected function should pass all the failing test cases provided.