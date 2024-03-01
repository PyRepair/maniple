### Bug Description:
The bug in the `convert_image` function arises from the incorrect handling of images with mode 'P' (palette) format. When the input image is in 'P' mode, the function should convert it to RGB mode. However, the function erroneously converts it to 'RGBA' mode due to an oversight in the if-else conditions.

### Fix Strategy:
To fix the bug, we need to adjust the conditional statement for images in 'P' mode to convert them to RGB mode correctly.

### Corrected Version of the Function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, image)
        image = background.convert('RGB')
    elif image.mode == 'P':  # Change this condition to handle 'P' mode images
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
``` 

This corrected version of the function should now properly handle images in 'P' mode and convert them to 'RGB' mode as needed.