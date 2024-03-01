### Bug Analysis
The bug is caused by the incorrect conversion of images in the `convert_image` function. Specifically, the issue lies in the condition `if image.format == 'PNG'` which is checking if the image format is PNG. However, the condition should be checking if the image format is not equal to 'JPEG' since the goal is to convert non-JPEG images to RGB format.

### Bug Fix Strategy
1. Change the condition `if image.format == 'PNG'` to `if image.format != 'JPEG'` to handle all non-JPEG image formats.
2. Update the logic accordingly to ensure that non-RGB images are converted to RGB format.

### Corrected Function
```python
def convert_image(self, image, size=None):
    if image.format != 'JPEG':
        if image.mode != 'RGB':
            image = image.convert('RGB')
    else:
        if image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0))
            image = background.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

By making these changes, the function should now correctly convert images to RGB format when needed.