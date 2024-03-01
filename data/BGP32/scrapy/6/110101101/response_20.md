### Bug Explanation
The bug in the `convert_image` function arises from the condition `if image.format == 'PNG' and image.mode == 'RGBA'` which tries to handle PNG images with RGBA mode by converting them to RGB. However, the issue occurs in the line `background.paste(image, image)` which incorrectly pastes the RGBA image onto a new RGBA image with a white background. This results in the loss of transparency information and leads to an incorrect conversion to RGB.

### Bug Fix Strategy
To fix this bug, we need to correctly handle the RGBA mode images by maintaining the transparency information during the conversion to RGB.

### Corrected Version of the Function
Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
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

By fixing the paste operation to include the alpha channel when pasting the RGBA image onto the new RGBA background, the transparency information is preserved correctly during the conversion to RGB, addressing the bug in the function.