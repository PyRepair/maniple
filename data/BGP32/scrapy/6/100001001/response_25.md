### Bug explanation
The bug in the provided function occurs when the input image is not in the 'RGB' mode and its format is not 'PNG'. In such cases, the function mistakenly converts the image to 'RGB' mode without checking the format. This leads to incorrect conversions and outputs in some cases.

### Bug fix strategy
To fix the bug, we need to ensure that when converting the image to 'RGB' mode, it only occurs if the image format is not 'PNG'. Additionally, we need to handle the situations where the input image is in a mode other than 'RGB' correctly.

### Corrected function
Here is the corrected version of the function:

```python
def convert_image(self, image, size=None):
    if image.mode != 'RGB':
        if image.format != 'PNG':
            image = image.convert('RGB')
        else:
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

This corrected version ensures that the image is only converted to 'RGB' mode if the format is not 'PNG' and handles other scenarios correctly.