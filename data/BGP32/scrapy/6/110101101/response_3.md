### Bug Explanation
The bug in the `convert_image` function lies in the condition and logic for handling PNG images with RGBA mode. When the input image is in PNG format and RGBA mode, the function tries to convert it to RGB mode by creating a new RGBA background image and then pasting the original image onto this background. However, when pasting the image, the code mistakenly uses `image` as the second argument to the `paste` method, which leads to an incorrect result.

### Bug Fix Strategy
To fix the bug, we need to replace `background.paste(image, image)` with `background.paste(image, (0, 0), image)`, ensuring that the original image is pasted onto the new background at the correct position. Additionally, we can simplify the logic by directly converting images to RGB when needed without separate handling for different modes.

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

By making this change, the `convert_image` function should now correctly handle PNG images with RGBA mode and produce the expected results, passing all the failing tests.