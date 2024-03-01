### Bug Explanation
The bug in the `convert_image` function arises from the incorrect handling of images with the format 'PNG' and mode 'RGBA'. The function is supposed to create a new image with a white background and paste the original image on top before converting it to 'RGB'. However, due to the buggy logic, the original image is pasted onto itself, leading to unexpected results.

### Bug Fix Strategy
To fix this bug, we need to correctly paste the original image onto the newly created white background image without affecting the original image. This can be achieved by creating a separate copy of the original image and pasting it onto the background.

### Corrected Version of the Function
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

By making this change, the corrected function should now properly handle images with the 'PNG' format and 'RGBA' mode without pasting the image onto itself. This should resolve the issues with the failing test cases.