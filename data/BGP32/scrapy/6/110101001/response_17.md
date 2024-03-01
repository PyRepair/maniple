### Bug Explanation
The bug in the `convert_image` function arises from the incorrect handling of images with mode 'RGBA' and format 'PNG'. The function has a condition that converts images with format 'PNG' and mode 'RGBA' to 'RGB' by creating a new image with a white background and pasting the original image onto it. However, the mistake lies in how the original image is pasted onto the background image. The correct method should be `background.paste(image, (0, 0))` instead of `background.paste(image, image)`. This results in the background image replacing itself with the original image, thus losing the intended result.

### Fix Strategy
To resolve the bug, we need to fix the line where the original image is pasted onto the background. By providing the correct coordinates for pasting, we can ensure that the original image is properly combined with the white background. Additionally, we should also update the condition to convert images with any mode other than 'RGB' to 'RGB' to cover all cases.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Paste the original image at (0,0)
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

By making these modifications, the `convert_image` function should now correctly handle different image modes and formats, passing the failing tests provided.