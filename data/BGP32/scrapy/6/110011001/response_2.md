### Analysis
1. The `convert_image` function is meant to convert images to RGB format and resize them if needed. The bug seems to be related to handling PNG images with RGBA mode.
2. The bug occurs when trying to convert an image with PNG format and RGBA mode to RGB and then saving it as JPEG. This causes transparency issues in the resulting image.
3. The bug is caused by converting PNG images with RGBA mode directly to RGB without properly handling the transparency. This results in incorrect colors when saving the image as JPEG.
4. To fix the bug, we need to handle transparency properly when converting PNG images with RGBA mode. One way to address this is by creating a white background layer for transparency. Then, composite the original image on top of the white background and convert it to RGB.
5. Below is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
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
``` 

By creating a white background and composite the original image onto it, the transparency issue when saving PNG images as JPEG should be resolved.