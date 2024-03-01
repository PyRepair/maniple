### Explanation:
The bug in the `convert_image` function stems from not handling images with an 'RGBA' mode correctly, specifically in the case where the format is 'PNG'. The current implementation attempts to convert the transparent image to RGB format but does not properly handle the alpha channel, resulting in incorrect color or transparency information in the converted image.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the logic in the `convert_image` function to properly handle images in 'RGBA' mode, especially when the format is 'PNG'. We need to ensure that the transparency information is preserved correctly when converting such images.

### The Corrected Version of the Function:
```python
def convert_image(self, image, size=None):
    if image.mode == 'RGBA':
        # Create a white background image with alpha channel
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
        # Composite the original image over the white background to fill alpha channel
        background.paste(image, (0, 0), image)
        # Convert the image with alpha channel to RGB while preserving alpha transparency
        image = background.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

### Updated Explanation:
In the corrected version of the `convert_image` function:
- We first check if the image mode is 'RGBA', indicating the presence of an alpha channel.
- If the image mode is 'RGBA', we create a white background image with an alpha channel, then paste the original image on this background to fill any transparency gaps.
- Next, we convert the composite image with the alpha channel to RGB format while preserving the alpha channel information.
- We proceed with the thumbnail and saving logic as before.

This update ensures that images with transparency are correctly handled during conversion, preserving the alpha transparency information in the resulting RGB image.