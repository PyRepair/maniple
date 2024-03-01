### Bug Explanation
The bug in the `convert_image` function arises from the condition that checks if the image format is 'PNG' and the mode is 'RGBA'. If the condition is met, a new RGBA image is created with a white background, the original image is pasted onto it, and then converted to RGB. The issue lies in the `background.paste(image, image)` line, where the `Image.paste()` method is being incorrectly used. This leads to an image that is not composed as intended, causing the subsequent conversions and thumbnail generation to produce incorrect results.

### Fix Strategy
To fix the bug, the correct way to paste the image onto the background is by providing a tuple specifying the position. This will ensure that the original image is correctly pasted onto the new background. Additionally, ensure that the `if size:` block is functioning correctly by properly maintaining the thumbnail's aspect ratio when resizing.

### Corrected Version
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

Applying this fix should ensure that the `convert_image` function behaves correctly and produces the expected results for the provided test cases.