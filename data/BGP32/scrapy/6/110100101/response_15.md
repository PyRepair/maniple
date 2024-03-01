#### Bug Explanation
The bug in the `convert_image` function arises from the condition `if image.format == 'PNG' and image.mode == 'RGBA'`. In this condition, the code is attempting to check if the image format is PNG and the mode is RGBA. However, this condition is not correctly handling the case when the image format is PNG and the mode is not RGBA. This causes unexpected behavior and leads to incorrect conversions.

#### Bug Fix Strategy
To fix the bug, we need to update the condition to correctly handle the scenarios where the image format is PNG but the mode is not RGBA. Additionally, adjustments should be made to ensure the conversion process is accurate and follows the expected outcomes outlined in the test cases.

#### Corrected Version of the `convert_image` Function
Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG':
        if image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background.convert('RGB')   
        else:
            image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making these adjustments, the `convert_image` function should now handle the conversion of PNG images with different modes correctly and align with the expected outcomes specified in the test cases.