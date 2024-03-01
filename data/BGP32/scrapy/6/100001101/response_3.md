### Bug Explanation
The bug in the provided function `convert_image()` lies in the condition for checking the image format and mode. In Case 1 and Case 2, the function incorrectly checks if the image format is 'PNG' and the mode is 'RGBA' when it should be checking for 'JPEG' and 'RGB' respectively. This leads to unnecessary conversion operations on the image.

In Case 3, the function correctly identifies the 'PNG' format and 'RGBA' mode, but the operation to paste the image onto a new background is incorrect. The `paste` method should be called with the same parameters as the `crop` method to preserve the image content.

In Case 4, when the image mode is not 'RGB', the function incorrectly converts the image to 'RGB'. This conversion should only be applied if the image format is 'PNG' and the mode is 'RGBA'.

### Fix Strategy
1. Update the condition to check if the image format is 'PNG' and mode is 'RGBA', and if so, correctly paste the image onto a new background in Case 3.
2. Correctly convert the image to 'RGB' only if the image format is 'PNG' and the mode is 'RGBA' in the else block.

### Corrected Function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0, image.size[0], image.size[1]))
        image = background.convert('RGB')
    elif image.format == 'PNG' and image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making these adjustments, the function should now correctly handle different image formats and modes according to the specified cases, producing the expected output in each scenario.