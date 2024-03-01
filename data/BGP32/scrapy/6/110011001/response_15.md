### Analysis
1. The `convert_image` function is meant to convert images to a specific format, including handling cases where the input image is in PNG format and RGBA mode.
2. The code contains conditional statements to check the format and mode of the input image and convert it accordingly. It also resizes the image if a specific size is provided.
3. The error occurs when converting an RGBA image with PNG format. The function should convert the image to RGB but there seems to be an issue with the conversion.
4. The bug seems to be related to the incorrect conversion of RGBA to RGB when the image format is PNG.
5. To fix the bug, we need to correctly handle the conversion of RGBA images with PNG format to RGB format.

### Bug Fix
Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG':
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
    else:
        # Handle conversion for other formats if needed
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
``` 

This corrected version will properly convert RGBA images with PNG format to RGB format before resizing and saving the image. It also covers the case where the input image format is not PNG.