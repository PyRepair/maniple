### Explanation:
The bug in the `convert_image` function arises from the incorrect handling of images with format 'PNG' and mode 'RGBA'. When the input image format is 'PNG' and mode is 'RGBA', the function attempts to convert it to a 'RGB' image but fails to do so correctly, leading to unexpected behavior. The issue occurs due to improper pasting of the original image onto a new white background before conversion.

### Bug Fix Strategy:
To fix the bug in the `convert_image` function, we need to ensure that the image with format 'PNG' and mode 'RGBA' is correctly converted to a 'RGB' image. This can be achieved by correctly pasting the original image on a new RGBA background and then converting it to RGB. Additionally, the function should return the correct image and buffer containing the image data.

### Corrected Version:
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
    buf.seek(0)  # Move the buffer cursor to the beginning
    return image, buf
``` 

By pasting the image onto a new RGBA background and then converting it to RGB, we address the bug and ensure proper conversion for 'PNG' images with 'RGBA' mode. Additionally, we adjust the buffer cursor position to the beginning before returning it.