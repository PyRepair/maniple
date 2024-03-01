### Bug Explanation
The bug in the `convert_image` function arises from the incorrect condition check for PNG images with RGBA mode. The current implementation checks if the image format is 'PNG' and mode is 'RGBA' to create a new background and convert the image to RGB. However, the condition should be based on the image type, not just the format.

### Bug Fix Strategy
To fix the bug, we need to modify the condition check to correctly identify PNG images with RGBA mode. We can check if the image is of type `PngImageFile` and has a mode of 'RGBA'. Additionally, we should handle the case where the image format is not 'PNG' but has a mode other than 'RGB'.

### Corrected Function
Here is the corrected version of the `convert_image` function:
```python
def convert_image(self, image, size=None):
    if isinstance(image, Image.Image):  # Check if image is an instance of Image.Image
        if isinstance(image, Image.PngImageFile) and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0))
            image = background.convert('RGB')
        elif not image.mode == 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
    else:
        return None, None
```

This corrected function properly handles the image type and mode to ensure correct conversion and thumbnail generation.