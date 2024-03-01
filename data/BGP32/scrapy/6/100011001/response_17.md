### Explanation:
The bug in the `convert_image` function lies in the condition where it checks if the image format is PNG and mode is RGBA. In this case, it creates a new RGBA background image and pastes the original image onto it. However, upon pasting the image, it is using `background.paste(image, image)`, which is incorrect due to the same name being used for the image object and the position where it should be pasted. This causes the new image to be completely overwritten with the original image.

### Bug Fix Strategy:
1. Check if the image format is PNG and mode is RGBA.
2. Create a new RGBA background image of the same size as the original image.
3. Paste the original image onto the background image.
4. Convert the background image to RGB.
5. Copy the image to prevent modifying the original.
6. If a size is provided, create a thumbnail of the specified size.
7. Save the image as a JPEG in a BytesIO buffer and return both the image and the buffer.

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

By fixing the paste operation in the RGBA PNG case to `background.paste(image, (0, 0))`, we ensure that the image is correctly pasted onto the background without being overwritten, resolving the bug in the function.