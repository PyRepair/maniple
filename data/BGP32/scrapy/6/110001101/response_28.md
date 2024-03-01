### Explanation of the bug
The bug in the `convert_image` function lies in the conditional check for image format and mode. When the image format is 'PNG' and mode is 'RGBA', the function is supposed to create a new RGBA background and then paste the original image onto it before converting the image to RGB. However, the bug occurs in the `background.paste(image, image)` line where the same `image` object is being used for both background creation and pasting. This results in an incorrect RGB conversion and ultimately affects the thumbnail generation as well.

### Strategy for fixing the bug
To fix the bug in the `convert_image` function, we need to ensure that a separate copy of the original image is used for pasting onto the background. This will prevent any side effects caused by modifying the original image object in place.

### Corrected version of the function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Corrected line: Paste the image at the top-left corner
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

This corrected version ensures that the original image is not modified during the creation of the background, and a proper RGB conversion is performed. It addresses the issue of incorrect image processing and thumbnail generation observed in the failing test cases.